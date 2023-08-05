#include <sys/time.h>

#include "intervaldb.h"

int C_int_max=INT_MAX; /* KLUDGE TO LET PYREX CODE ACCESS VALUE OF INT_MAX MACRO */

unsigned long gstart[25] = {0, 15940, 31520, 44280, 56520, 68190, 79180, 89440, 
        98810, 107670, 116280, 124990, 133570, 140870, 147710, 154220, 160050,
        165420, 170580, 174400, 178550, 181530, 184770, 194650, 198160};

int imstart_qsort_cmp(const void *void_a,const void *void_b)
{ /* STRAIGHTFORWARD COMPARISON OF SIGNED start VALUES, LONGER INTERVALS 1ST */
  IntervalMap *a=(IntervalMap *)void_a,*b=(IntervalMap *)void_b;
  if (a->start<b->start)
    return -1;
  else if (a->start>b->start)
    return 1;
  else if (a->end>b->end) /* SAME START: PUT LONGER INTERVAL 1ST */
    return -1;
  else if (a->end<b->end) /* CONTAINED INTERVAL SHOULD FOLLOW LARGER INTERVAL*/
    return 1;
  else
    return 0;
}

#ifdef MERGE_INTERVAL_ORIENTATIONS
int im_qsort_cmp(const void *void_a,const void *void_b)
{ /* MERGE FORWARD AND REVERSE INTERVALS AS IF THEY WERE ALL IN FORWARD ORI */
  int a_start,a_end,b_start,b_end;
  IntervalMap *a=(IntervalMap *)void_a,*b=(IntervalMap *)void_b;
  SET_INTERVAL_POSITIVE(*a,a_start,a_end);
  SET_INTERVAL_POSITIVE(*b,b_start,b_end);
  if (a_start<b_start)
    return -1;
  else if (a_start>b_start)
    return 1;
  else if (a_end>b_end) /* SAME START: PUT LONGER INTERVAL 1ST */
    return -1;
  else if (a_end<b_end) /* CONTAINED INTERVAL SHOULD FOLLOW LARGER INTERVAL*/
    return 1;
  else
    return 0;
}
#endif

int sublist_qsort_cmp(const void *void_a,const void *void_b)
{ /* SORT IN SUBLIST ORDER, SECONDARILY BY start */
  IntervalMap *a=(IntervalMap *)void_a,*b=(IntervalMap *)void_b;
  if (a->sublist<b->sublist)
    return -1;
  else if (a->sublist>b->sublist)
    return 1;
  else if (START_POSITIVE(*a) < START_POSITIVE(*b))
    return -1;
  else if (START_POSITIVE(*a) > START_POSITIVE(*b))
    return 1;
  else
    return 0;
}

SublistHeader *build_nested_list_inplace(IntervalMap im[],int n,
					 int *p_n,int *p_nlists)
{
  int i=0,parent,nlists=1,isublist=0,total=0,temp=0;
  SublistHeader *subheader=NULL;

#ifdef ALL_POSITIVE_ORIENTATION
  reorient_intervals(n,im,1); /* FORCE ALL INTERVALS INTO POSITIVE ORI */
#endif
#ifdef MERGE_INTERVAL_ORIENTATIONS
  qsort(im,n,sizeof(IntervalMap),im_qsort_cmp); /* SORT BY start, CONTAINMENT */
#else
  qsort(im,n,sizeof(IntervalMap),imstart_qsort_cmp); /* SORT BY start, CONTAINMENT */
#endif
  nlists=1;
  for(i=1;i<n;++i){
    if(!(END_POSITIVE(im[i])>END_POSITIVE(im[i-1]) /* i NOT CONTAINED */
	 || (END_POSITIVE(im[i])==END_POSITIVE(im[i-1]) /* SAME INTERVAL! */
	     && START_POSITIVE(im[i])==START_POSITIVE(im[i-1])))){
      nlists++;
/*       printf("%d (%d,%d) -> (%d,%d) %d\n", nlists, im[i-1].start, */
/* 	     im[i-1].end, im[i].start,im[i].end,i); */
    }
  }

/*   printf("%d lists?!\n", nlists); */
  *p_nlists=nlists-1;

  if(nlists==1){
    *p_n=n;
    //subheader = calloc(1,sizeof(SublistHeader));
    CALLOC(subheader,1,SublistHeader); /* RETURN A DUMMY ARRAY, SINCE NULL RETURN IS ERROR CODE */
    return subheader;
  }
  //subheader = calloc(nlists+1,sizeof(SublistHeader));
  CALLOC(subheader,nlists+1,SublistHeader); /* SUBLIST HEADER INDEX */

  im[0].sublist=0;
  subheader[0].start= -1;
  subheader[0].len=1;
  parent=0;
  nlists=1;
  isublist=1;
  for(i=1;i<n;){
    if(isublist && (END_POSITIVE(im[i])>END_POSITIVE(im[parent]) /* i NOT CONTAINED */
		    || (END_POSITIVE(im[i])==END_POSITIVE(im[parent]) /* SAME INTERVAL! */
			&& START_POSITIVE(im[i])==START_POSITIVE(im[parent])))){
      subheader[isublist].start=subheader[im[parent].sublist].len-1; /* RECORD PARENT RELATIVE POSITION */
      isublist=im[parent].sublist;
      parent=subheader[im[parent].sublist].start;
    }
    else{
      if(subheader[isublist].len==0){
	nlists++;
      }
      subheader[isublist].len++;
      im[i].sublist=isublist;
      parent=i;
      isublist=nlists;
      subheader[isublist].start=parent;
      i++;
    }
  }

  while(isublist>0){ /* pop remaining stack */
    subheader[isublist].start=subheader[im[parent].sublist].len-1; /* RECORD PARENT RELATIVE POSITION */
    isublist=im[parent].sublist;
    parent=subheader[im[parent].sublist].start;
  }

  *p_n=subheader[0].len;

  total=0;
  for(i=0;i<nlists+1;++i){
    temp=subheader[i].len;
    subheader[i].len=total;
    total+=temp;
  };

  /* SUBHEADER.LEN IS NOW START OF THE SUBLIST */

  for(i=1;i<n;i+=1){
    if(im[i].sublist>im[i-1].sublist){
      subheader[im[i].sublist].start+=subheader[im[i-1].sublist].len;
    }
  }

  /* SUBHEADER.START IS NOW ABS POSITION OF PARENT */

  qsort(im,n,sizeof(IntervalMap),sublist_qsort_cmp);
  /* AT THIS POINT SUBLISTS ARE GROUPED TOGETHER, READY TO PACK */

  isublist=0;
  subheader[0].start=0;
  subheader[0].len=0;
  for(i=0;i<n;++i){
    if(im[i].sublist>isublist){
/*       printf("Entering sublist %d (%d,%d)\n", im[i].sublist, im[i].start,im[i].end); */
      isublist=im[i].sublist;
      parent=subheader[isublist].start;
/*       printf("Parent (%d,%d) is at %d, list start is at %d\n",  */
/* 	     im[parent].start, im[parent].end, subheader[isublist].start,i); */
      im[parent].sublist=isublist-1;
      subheader[isublist].len=0;
      subheader[isublist].start=i;
    }
    subheader[isublist].len++;
    im[i].sublist= -1;
  }

    nlists--;
    memmove(subheader,subheader+1,nlists*sizeof(SublistHeader));

    return subheader;
    handle_malloc_failure:
    /* FREE ANY MALLOCS WE PERFORMED*/
    FREE(subheader);
    return NULL;
}



SublistHeader *build_nested_list(IntervalMap im[],int n,
				 int *p_n,int *p_nlists)
{
  int i=0,j,k,parent,nsub=0,nlists=0;
  IntervalMap *imsub=NULL;
  SublistHeader *subheader=NULL;

#ifdef ALL_POSITIVE_ORIENTATION
  reorient_intervals(n,im,1); /* FORCE ALL INTERVALS INTO POSITIVE ORI */
#endif
#ifdef MERGE_INTERVAL_ORIENTATIONS
  qsort(im,n,sizeof(IntervalMap),im_qsort_cmp); /* SORT BY start, CONTAINMENT */
#else
  qsort(im,n,sizeof(IntervalMap),imstart_qsort_cmp); /* SORT BY start, CONTAINMENT */
#endif
  while (i<n) { /* TOP LEVEL LIST SCAN */
    parent=i;
    i=parent+1;
    while (i<n && parent>=0) { /* RECURSIVE ALGORITHM OF ALEX ALEKSEYENKO */
      if (END_POSITIVE(im[i])>END_POSITIVE(im[parent]) /* i NOT CONTAINED */
	  || (END_POSITIVE(im[i])==END_POSITIVE(im[parent]) /* SAME INTERVAL! */
	      && START_POSITIVE(im[i])==START_POSITIVE(im[parent])))
	parent=im[parent].sublist; /* POP RECURSIVE STACK*/
      else  { /* i CONTAINED IN parent*/
	im[i].sublist=parent; /* MARK AS CONTAINED IN parent */
	nsub++; /* COUNT TOTAL #SUBLIST ENTRIES */
	parent=i; /* AND PUSH ONTO RECURSIVE STACK */
	i++; /* ADVANCE TO NEXT INTERVAL */
      }
    }
  } /* AT THIS POINT sublist IS EITHER -1 IF NOT IN SUBLIST, OR INDICATES parent*/

  if (nsub>0) { /* WE HAVE SUBLISTS TO PROCESS */
    CALLOC(imsub,nsub,IntervalMap); /* TEMPORARY ARRAY FOR REPACKING SUBLISTS */
    for (i=j=0;i<n;i++) { /* GENERATE LIST FOR SORTING; ASSIGN HEADER INDEXES*/
      parent=im[i].sublist;
      if (parent>=0)  {/* IN A SUBLIST */
	imsub[j].start=i;
	imsub[j].sublist=parent;
	j++;
	if (im[parent].sublist<0) /* A NEW PARENT! SET HIS SUBLIST HEADER INDEX */
	  im[parent].sublist=nlists++;
      }
      im[i].sublist= -1; /* RESET TO DEFAULT VALUE: NO SUBLIST */
    }
    qsort(imsub,nsub,sizeof(IntervalMap),sublist_qsort_cmp);
    /* AT THIS POINT SUBLISTS ARE GROUPED TOGETHER, READY TO PACK */

    CALLOC(subheader,nlists,SublistHeader); /* SUBLIST HEADER INDEX */
    for (i=0;i<nsub;i++) { /* COPY SUBLIST ENTRIES TO imsub */
      j=imsub[i].start;
      parent=imsub[i].sublist;
      memcpy(imsub+i,im+j,sizeof(IntervalMap)); /* COPY INTERVAL */
      k=im[parent].sublist;
      if (subheader[k].len==0) /* START A NEW SUBLIST */
	subheader[k].start=i;
      subheader[k].len++; /* COUNT THE SUBLIST ENTRIES */
      im[j].start=im[j].end= -1; /* MARK FOR DELETION */
    } /* DONE COPYING ALL SUBLISTS TO imsub */

    for (i=j=0;i<n;i++) /* COMPRESS THE LIST TO REMOVE SUBLISTS */
      if (im[i].start!= -1 || im[i].end!= -1) { /* NOT IN A SUBLIST, SO KEEP */
	if (j<i) /* COPY TO NEW COMPACTED LOCATION */
	  memcpy(im+j,im+i,sizeof(IntervalMap));
	j++;
      }

    memcpy(im+j,imsub,nsub*sizeof(IntervalMap)); /* COPY THE SUBLISTS */
    for (i=0;i<nlists;i++) /* ADJUST start ADDRESSES FOR SHIFT*/
      subheader[i].start += j;
    FREE(imsub);
    *p_n = j; /* COPY THE COMPRESSED LIST SIZES BACK TO CALLER*/
  }
  else {  /* NO SUBLISTS: HANDLE THIS CASE CAREFULLY */
    *p_n = n;
    CALLOC(subheader,1,SublistHeader); /* RETURN A DUMMY ARRAY, SINCE NULL RETURN IS ERROR CODE */
  }
  *p_nlists=nlists; /* RETURN COUNT OF NUMBER OF SUBLISTS */
  return subheader;
 handle_malloc_failure:
  FREE(imsub);  /* FREE ANY MALLOCS WE PERFORMED*/
  FREE(subheader);
  return NULL;
}


IntervalMap *interval_map_alloc(int n)
{
  IntervalMap *im=NULL;
  CALLOC(im,n,IntervalMap);
  return im;
 handle_malloc_failure:
  return NULL;
}

int find_overlap_start(int start,int end,IntervalMap im[],int n)
{
    //printf("Line 280: %i, %i, %i\n", start, end, n);
  int l=0,mid,r;

  r=n-1;
  while (l<r) {
    mid=(l+r)/2;
    if (END_POSITIVE(im[mid])<=start)
      l=mid+1;
    else
      r=mid;
  }
  //printf("  %i\n", l);
  if (l<n && HAS_OVERLAP_POSITIVE(im[l],start,end))
    return l; /* l IS START OF OVERLAP */
  else
    return -1; /* NO OVERLAP FOUND */
}

int find_index_start(int start,int end,IntervalIndex im[],int n)
{
  int l=0,mid,r;

  r=n-1;
  while (l<r) {
    mid=(l+r)/2;
    if (END_POSITIVE(im[mid])<=start)
      l=mid+1;
    else
      r=mid;
  }
  return l; /* l IS START OF POSSIBLE OVERLAP */
}

int find_suboverlap_start(int start,int end,int isub,IntervalMap im[],
			  SublistHeader subheader[],int nlists)
{
  int i;

  if (isub>=0) {
    i=find_overlap_start(start,end,im+subheader[isub].start,subheader[isub].len);
    if (i>=0)
      return i+subheader[isub].start;
  }
  return -1;
}


IntervalIterator *interval_iterator_alloc(void)
{
  IntervalIterator *it=NULL;
  CALLOC(it,1,IntervalIterator);
  return it;
 handle_malloc_failure:
  return NULL;
}

int free_interval_iterator(IntervalIterator *it)
{
  IntervalIterator *it2,*it_next;
  if (!it)
    return 0;
  FREE_ITERATOR_STACK(it,it2,it_next);
  return 0;
}


IntervalIterator *reset_interval_iterator(IntervalIterator *it)
{
  ITERATOR_STACK_TOP(it);
  it->n=0;
  return it;
}


void reorient_intervals(int n,IntervalMap im[],int ori_sign)
{
  int i,tmp;
  for (i=0;i<n;i++) {
    if ((im[i].start>=0 ? 1:-1)!=ori_sign) { /* ORIENTATION MISMATCH */
      tmp=im[i].start; /* SO REVERSE THIS INTERVAL MAPPING */
      im[i].start= -im[i].end;
      im[i].end =  -tmp;
      /* tmp=im[i].target_start; */
      /* im[i].target_start= -im[i].target_end; */
      /* im[i].target_end =  -tmp; */
    }
  }
}

int find_intervals(IntervalIterator *it0,int start,int end,
		   IntervalMap im[],int n,
		   SublistHeader subheader[],int nlists,
		   IntervalMap buf[],int nbuf,
		   int *p_nreturn,IntervalIterator **it_return)
{
  IntervalIterator *it=NULL,*it2=NULL;
  int ibuf=0,j,k,ori_sign=1;
  if (!it0) { /* ALLOCATE AN ITERATOR IF NOT SUPPLIED*/
    CALLOC(it,1,IntervalIterator);
  }
  else
    it=it0;

#if defined(ALL_POSITIVE_ORIENTATION) || defined(MERGE_INTERVAL_ORIENTATIONS)
  if (start<0) { /* NEED TO CONVERT TO POSITIVE ORIENTATION */
    j=start;
    start= -end;
    end= -j;
    ori_sign = -1;
  }
#endif
  if (it->n == 0) { /* DEFAULT: SEARCH THE TOP NESTED LIST */
    j = subheader[0].start;      
    it->n=n;
    it->i=find_overlap_start(start,end,im,n);   
  }
  do {    
    while (it->i>=0 && it->i<it->n && HAS_OVERLAP_POSITIVE(im[it->i],start,end)) {
      memcpy(buf+ibuf,im + it->i,sizeof(IntervalMap)); /*SAVE THIS HIT TO BUFFER */
      ibuf++;
      k=im[it->i].sublist; /* GET SUBLIST OF i IF ANY */
      it->i++; /* ADVANCE TO NEXT INTERVAL */
      if (k>=0 && (j=find_suboverlap_start(start,end,k,im,subheader,nlists))>=0) {
        PUSH_ITERATOR_STACK(it,it2,IntervalIterator); /* RECURSE TO SUBLIST */
        it2->i = j; /* START OF OVERLAPPING HITS IN THIS SUBLIST */
        it2->n = subheader[k].start+subheader[k].len; /* END OF SUBLIST */
        it=it2; /* PUSH THE ITERATOR STACK */
      }
      if (ibuf>=nbuf){ /* FILLED THE BUFFER, RETURN THE RESULTS SO FAR */
        goto finally_return_result;
      }
    }
  } while (POP_ITERATOR_STACK(it));  /* IF STACK EXHAUSTED,  EXIT */
  if (!it0) /* FREE THE ITERATOR WE CREATED.  NO NEED TO RETURN IT TO USER */
    free_interval_iterator(it);
  it=NULL;  /* ITERATOR IS EXHAUSTED */

 finally_return_result:
#if defined(ALL_POSITIVE_ORIENTATION) || defined(MERGE_INTERVAL_ORIENTATIONS)
  reorient_intervals(ibuf,buf,ori_sign); /* REORIENT INTERVALS TO MATCH QUERY ORI */
#endif

  *p_nreturn=ibuf; /* #INTERVALS FOUND IN THIS PASS */
  *it_return=it; /* HAND BACK ITERATOR FOR CONTINUING THE SEARCH, IF ANY */
  return 0; /* SIGNAL THAT NO ERROR OCCURRED */
 handle_malloc_failure:
  return -1;
}


int repack_subheaders(IntervalMap im[],int n,int div,
		      SublistHeader *subheader,int nlists)
{
  int i,j,*sub_map=NULL;
  SublistHeader *sub_pack=NULL;

  CALLOC(sub_map,nlists,int);
  CALLOC(sub_pack,nlists,SublistHeader);
  for (i=j=0;i<nlists;i++) { /* PLACE SUBLISTS W/ len>div AT FRONT */
    if (subheader[i].len>div) {
      memcpy(sub_pack+j,subheader+i,sizeof(SublistHeader));
      sub_map[i]=j;
      j++;
    }
  }
  for (i=0;i<nlists;i++) { /* PLACE SUBLISTS W/ len<=div AFTERWARDS */
    if (subheader[i].len<=div) {
      memcpy(sub_pack+j,subheader+i,sizeof(SublistHeader));
      sub_map[i]=j;
      j++;
    }
  }
  for (i=0;i<n;i++) /* ADJUST im[].sublist TO THE NEW LOCATIONS */
    if (im[i].sublist>=0)
      im[i].sublist=sub_map[im[i].sublist];
  memcpy(subheader,sub_pack,nlists*sizeof(SublistHeader)); /* SAVE REORDERED LIST*/

  FREE(sub_map);
  FREE(sub_pack);
  return 0;
 handle_malloc_failure:
  return -1;
}

int free_interval_dbfile(IntervalDBFile *db_file)
{
  if (db_file->ifile_idb)
    fclose(db_file->ifile_idb);
#ifdef ON_DEMAND_SUBLIST_HEADER
  if (db_file->subheader_file.ifile)
    fclose(db_file->subheader_file.ifile);
#endif
  FREE(db_file->ii);
  FREE(db_file->subheader);
  free(db_file);
  return 0;
}


IntervalMap *read_intervals(int n,FILE *ifile) 
{ 
   int i=0; 
   IntervalMap *im=NULL; 
   CALLOC(im,n,IntervalMap); // ALLOCATE THE WHOLE ARRAY  
   while (i<n && fscanf(ifile," %d %d %d %d %d",&im[i].start,&im[i].end, 
 		       &im[i].target_id,&im[i].start, 
 		       &im[i].end)==5) { 
     im[i].sublist= -1; // DEFAULT: NO SUBLIST  
     i++; 
   } 
    if (i!=n) { 
        fprintf(stderr,"WARNING: number of records read %d does not match allocation %d",i,n); 
    } 
    return im; 
    handle_malloc_failure: 
    return NULL; //NO CLEANUP ACTIONS REQUIRED  
}

IntervalMap** openBed24(char* bFile, int* nD)
{   //open a .bed file and construct g_data  
    char buf[1024];
    int i, k, ichr, lens;    
    char *s1, *s2, *s3;   
    FILE* fd = fopen(bFile, "r"); 
    while(fgets(buf, 1024, fd)!=NULL){
        s1 = strtok(buf, "\t"); 
        lens = strlen(s1);   
        if(lens > 5 || lens < 4)
            ichr = -1;  
        else if(strcmp(s1, "chrX")==0)
            ichr = 22;
        else if(strcmp(s1, "chrY")==0)
            ichr = 23;     
        else if (strcmp(s1, "chrM")==0)
            ichr = -1;    
        else{
            ichr = (int)(atoi(&s1[3])-1);
        }     
        if(ichr>=0)
            nD[ichr]++;
    }	
    fseek(fd, 0, SEEK_SET);
    //-------------------------------------------------------------------------   
    IntervalMap** im = malloc(24*sizeof(IntervalMap*));
    for(i=0;i<24;i++){
        im[i] = NULL;
        if(nD[i]>0)
            CALLOC(im[i], nD[i], IntervalMap);
        nD[i]=0;
    }
    while (fgets(buf, 1024, fd)) {
        s1 = strtok(buf, "\t");
        s2 = strtok(NULL, "\t");
        s3 = strtok(NULL, "\t");   
        lens = strlen(s1);   
        if(lens > 5 || lens < 4)
            ichr = -1;  
        else if(strcmp(s1, "chrX")==0)
            ichr = 22;
        else if(strcmp(s1, "chrY")==0)
            ichr = 23;     
        else if (strcmp(s1, "chrM")==0)
            ichr = -1;    
        else{
            ichr = (int)(atoi(&s1[3])-1);
        }          
        if(ichr>=0){
            k = nD[ichr];
            im[ichr][k].start  = atol(s2);
            im[ichr][k].end  = atol(s3);
            im[ichr][k].target_id = atol(s2); 
            im[ichr][k].sublist = -1;
            nD[ichr]++;
        }     
    } 
    fclose(fd);
    return im;  
} 

#define LINE_LEN 1024
int main(int argc, char **argv) {
    if(argc!=3){
        printf("input: data file, query file \n");
        return 0;		    
    }
    clock_t start1, end1, end2;
    start1 = clock();     
    int i, j, ichr;
    char *qfile = argv[1];
    char *dfile = argv[2];
    char *s1, *s2, *s3;
    FILE *fp;
    char line[LINE_LEN];
    int start, end;
    //-------------------------------------------------------------------------
    int interval_map_size = 1024; 
    int* nD = calloc(24, sizeof(int));
    IntervalMap **im = openBed24(dfile, nD);
    SublistHeader **sh = malloc(24*sizeof(SublistHeader*)); 
    int **p_n = malloc(24*sizeof(int*)); 
    int **p_nlists = malloc(24*sizeof(int*)); 
    int **nhits = malloc(24*sizeof(int*));    
    uint64_t Total=0;  
    for(i=0;i<24;i++){
        p_n[i] = malloc(1*sizeof(int));
        p_nlists[i] = malloc(1*sizeof(int));
        nhits[i] = malloc(1*sizeof(int));
        if(nD[i]>0){
            sh[i] = build_nested_list(im[i], nD[i], p_n[i], p_nlists[i]); 
            //printf("%i:\t%i\t%i\t%i\n", i, nD[i], *p_n[i], *p_nlists[i]);
            //for(j=0;j<nD[i];j++)
            //    printf("%i:\t%i\t%i\t%i\n", j, im[i][j].start, im[i][j].end, im[i][j].sublist);
            
            //for(j=0;j<*p_nlists[i];j++)
            //    printf("%i:\t%i\t%i\n",j, sh[i][j].start, sh[i][j].len);
            //printf("*p_n %d\n", *p_n[i]); 
            //printf("*p_nlists %d\n", *p_nlists[i]);   
        }
    }  
    //-------------------------------------------------------------------------
    end1 = clock();      
    //printf("Time for construction: %f \n", ((double)(end1-start1))/CLOCKS_PER_SEC);   
    fp = fopen(qfile, "r");
    if (fp == NULL) {
        printf("File %s not found!\n", qfile);
        return 0;
    }    
   
    IntervalIterator *it;
    IntervalIterator *it_alloc;    
    IntervalMap im_buf[1024];  
    uint32_t qhits;  
    while (fgets(line, LINE_LEN, fp)) {
        s1 = strtok(line, "\t");
        s2 = strtok(NULL, "\t");
        s3 = strtok(NULL, "\t");
        if(strlen(s1)>5 || strlen(s1)<4 || strcmp(s1, "chrM")==0)
            ichr = -1;  
        else if(strcmp(s1, "chrX")==0)
            ichr = 22;
        else if(strcmp(s1, "chrY")==0)
            ichr = 23;         
        else{
            ichr = (int)(atoi(&s1[3])-1);
        }    
        if(ichr>=0){
            qhits = 0;
            start = atol(s2);			
            end   = atol(s3);//the definition is different!	  
            //-----------------------------------------------------------------
            it_alloc = interval_iterator_alloc();     
            it = it_alloc;
            while(it){  
                find_intervals(it, start, end, im[ichr], *p_n[ichr], sh[ichr], *p_nlists[ichr], im_buf, 1024, nhits[ichr], &it); 
                //printf("nhits %d\n", *nhits[ichr]); 
                qhits += *nhits[ichr];        
                //for (i = 0; i < *nhits[ichr]; i++){ 
                //    printf("\t%d\t%d\n", im_buf[i].start, im_buf[i].end); 
                //}
            }
            free_interval_iterator(it_alloc);
            Total += qhits;
            printf("%s\t%ld\t%ld\t%i\n", s1, atol(s2), atol(s3), qhits);            
        }
    }
    fclose(fp);
    end2 = clock();    

    //printf("Total: %lld\n", (long long)Total);
    for(i=0;i<24;i++){
        free(p_n[i]);
        free(p_nlists[i]);
        free(nhits[i]);
    }   
    free(p_n); 
    free(p_nlists); 
    free(nhits);  
    free(nD);
} 
