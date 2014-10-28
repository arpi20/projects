#include<dirent.h>
#include<stdio.h>
#include<iostream>
#include<ctype.h>
#include<cstdio>
#include<cstdlib>
#include<algorithm>
#include<vector>
#include<set>
#include<map>
#include<string>
#include<string.h>
#include<cstring>
#include<stack>
#include<queue>
#include<cassert>
#include<iterator>
#include<cmath>
#include <fstream>
#define _LARGEFILE64_SOURCE /* See feature_test_macros(7) */
#include <sys/types.h>
#include <unistd.h> 
#include "rapidxml-1.13/rapidxml.hpp"
#define _FILE_OFFSET_BITS 64
using namespace rapidxml;
using namespace std;
extern int stem( char* s, int i, int j);
int QMX=1000;
FILE* ff;
map < string, long long int > idx;  // for storing the secondary index

map < string, long long int >::iterator itidx;

map <string,char> query;  /// for storing in which filed we have to look for the query.

map <string,char>::iterator itq;

FILE* fout;
FILE* fin;
FILE* f1, *f2 ,*f3;
FILE* fdtitle1;
struct docnode{
	int docId;
	double w;
	int count;
};
typedef struct docnode docnode;
bool operator<(docnode i,docnode j){
	return i.docId < j.docId;
}

int compare(docnode i,docnode j ){
	if(i.count > j.count){
		return 1;
	}
	else if(i.count==j.count){
		if(i.w > j.w ){
			return 1;
		}
		return 0;
	}
	return 0;
}

map <string, vector< docnode > > postl_words;  /// posting list for each word of the query.

map <string, vector< docnode > >::iterator itwp;

priority_queue< docnode > prio_heap;

vector< docnode> results;

vector< docnode>::iterator itresults;
void search( string w ){
        itidx = idx.lower_bound( w );
        unsigned long long int  pos=0;
        long long int  temppos;
        char word[1000] = {'\0'};
        if( itidx->first == w ){
            fseeko64( f2, itidx->second , SEEK_SET);
            fscanf(f2,"%s",word);
            fscanf(f2,"%lld",&pos);
        }
        else{
            if( itidx == idx.begin()){
            }
            else{
                itidx--;
                fseeko64( f2, itidx->second , SEEK_SET);

                while(1){

                    if( fscanf(f2,"%s",word) == EOF ) break;
                    fscanf(f2,"%lld",&temppos);
                    int flag = strcmp( word , w.c_str());
                    if( flag > 0 ) break;
                    if( flag == 0 ){
                        pos = temppos;
                        break;	
                    }
                }   
            }
        }
        if( pos != -1 ){
            vector<docnode> postings; 
	    printf("%lld\n",pos);
            fseeko64(f3,pos,SEEK_SET);
       //     _fseeki64(f3,pos,SEEK_SET );
	   // lseek64(f3, pos, SEEK_SET);
	  //  _lseeki64(f3, pos, SEEK_SET);
            fscanf(f3,"%s",word);
           int docId;
            char c;
            while( 1 ){
                char cat[100];
                fscanf(f3,"%d",&docId);
                fscanf(f3,"%s",cat);
                fscanf(f3,"%c",&c);
		char* p = cat;
		int freq=0;
		if(query[w]=='n'){
			freq=0;
			while(*p!='\0'){
				p++;
				while( *p !='\0' && *p >='0' && *p<='9'){
					freq = 10*freq + *p - 48;
					p++;
				}
			}
			docnode docpair;
			docpair.docId  = docId ;
			docpair.w = (double ) freq;
			docpair.count=1;
			postings.push_back(docpair);

		}
		else{

			while( *p != '\0' ){
				if( (*p+32) == query[w] ){
					freq = 0;
					p++;
					while( *p !='\0' && *p >='0' && *p<='9'){
						freq = 10*freq + *p - 48;
						p++;
					}
					if( query[w] == 't' ){
						freq *= 20;   // title is given more weight
					}
					else if( query[w] == 'o'){
						freq *= 5;   

					}
					else if( query[w] == 'i'){
						freq *= 15;   

					}
					else if( query[w] == 'c'){
						freq *= 10;   
					}
					docnode docpair;
					docpair.docId  = docId ;
					docpair.w = (double ) freq;
					docpair.count=1;   // number of times this doc occurs.
					postings.push_back( docpair );
				}
				else p++;
			}
		}
                if( c == '\n') break;
            }
            postl_words[ w ] = postings;
        }
}
bool process_query(){
    printf("Search ::: ");
    char q[QMX];
    if( scanf("%[^\n]",q) == EOF ) return 1;
    getchar();
    char *x=strstr(q,":");
    postl_words.clear();
    query.clear();
    if(x==NULL){
	    char* pch = strtok (q," ");
	    int i=0;
	    char tchar[1000];
	    query.clear();
	    postl_words.clear();
	    while(pch != NULL)
	    {   
		    i++;
		    strcpy( tchar , pch );
		    printf("%s\n",tchar);
		    int len = 0;
		    for(char* temp = tchar; *temp!='\0';temp++,len++){
			    if( *temp >='A' && *temp<='Z') *temp += 32;
		    }
		    tchar[ stem( tchar,0,len-1 ) + 1 ] = '\0';
		    string temp = tchar;
		    query[temp] = 'n';
		    pch = strtok (NULL," ");
	    }
    }
    else{
	    char* pch = strtok (q," :");
	    int i=0;
	    char tchar[1000];
	    char attr;
	    query.clear();
	    postl_words.clear();
	    while(pch != NULL)
	    {   
		    i++;
		    strcpy( tchar , pch );
		    int len = 0;
		    for(char* temp = tchar; *temp!='\0';temp++,len++){
			    if( *temp >='A' && *temp<='Z') *temp += 32;
		    }
		    tchar[ stem( tchar,0,len-1 ) + 1 ] = '\0';  // stemming
		    if( i&1 ){ 
			    attr = tchar[0];
			    if( attr == 'b' ) attr = 'b';
		    }
		    else{
			    string temp = tchar;
			    query[temp] = attr;
		    }
		    pch = strtok (NULL," :");
	    }
    }
    return 0;
}
void give_title( int d){
    char buffer[1000];
    int docId;
    char c;
    fdtitle1 = fopen64("title_to_docid_index","r");
    fseeko64( fdtitle1 , 0 , SEEK_SET);
    while(1){
        if(fscanf(fdtitle1, "%d%c",&docId, &c)== EOF) break;
        fscanf(fdtitle1, "%[^\n]",buffer);
        if( docId == d ) {
            printf("%s\n",buffer);
            break;
        }
    }
}
void give_results(){
    fdtitle1 = fopen64("title_to_docid_index","r");
    int i =0;
    for( itresults = results.begin() ; itresults != results.end() ; itresults++){
//	    printf("%d\n",itresults->docId);
        give_title( itresults->docId  );
        i++;
        if( i == 15 ) break;
    }   
   fclose( fdtitle1 );
}
void prim_ind(char* infile, char* outfile , int gaps){
    fin = fopen(infile,"r");
    fout = fopen(outfile , "w");
    char word[1000];
    long long int pos;
    int i;
    char c;
    int docId;
    int counter = 0;
    char cat[1000];
    while(1){
        pos = ftell( fin );
        if( fscanf(fin , "%s",word) == EOF ) break;
        while(1){
            fscanf(fin,"%c",&c);
            if( c == '\n') break;
            if( fscanf(fin,"%s",cat) == EOF) break;
        }
        if(counter%gaps==0) fprintf(fout,"%s %lld\n",word , pos ); 
        counter++;
    }
    fprintf(fout,"%s %lld\n","{}",pos);
    fclose(fin);
    fclose(fout);
}
void second_ind(char* infile, char* outfile , int gaps){
    fin = fopen(infile,"r");
    fout = fopen(outfile , "w");
    char word[1000];
    long long int  pos;
    long long temp;
    int i;
    char c;
    int counter = 0;
    while(1){
        pos = ftell( fin );
        if( fscanf(fin,"%s",word) == EOF ) break;
        fscanf(fin,"%lld",&temp);
        fscanf(fin,"%c",&c);
        if(counter%gaps==0) fprintf(fout,"%s %lld\n",word , pos ); 
        counter++;
    }
    fprintf(fout,"%s %lld\n","{}",pos);
    fclose(fin);
    fclose(fout);
}

int main(int argc , char* argv[]){
//	if( argc < 4 ) exit(1);
//	prim_ind(argv[3] , argv[2] , 1);
//	second_ind( argv[2] , argv[1] , 100 );
	//fin = fopen(argv[1],"r");
	fin = fopen64("aa","r");
	char word[1000];
	long long int  pos;
	int i;
	char c;
	while(1){
		if( fscanf(fin,"%s",word) == EOF ) break;
		fscanf(fin,"%lld",&pos);
		string tword = word;
		idx[tword] = pos;
	}
	fclose(fin);
	//printf("idx\n");

        f1 = fopen64("aa","r");
	f2 = fopen64("bb","r");
	f3 = fopen64("final_index","r");
	if(f3==NULL){
		printf("cannot open\n");
	}
	else{
        /*f1 = fopen(argv[1],"r");
	f2 = fopen(argv[2],"r");
	f3 = fopen(argv[3],"r");*/
	//printf("idx\n");
	while(1){
		if( process_query() ) break;
		for(itq = query.begin(); itq != query.end() ; itq++){
			search( itq->first );
		}
		results.clear();
		for(itwp=postl_words.begin();itwp!=postl_words.end();itwp++){
			for(int i=0;i<itwp->second.size();i++){
				prio_heap.push(itwp->second[i] );
			}
		}
		while( !prio_heap.empty() ){
			docnode cur = prio_heap.top();
			prio_heap.pop();
			while( !prio_heap.empty() && prio_heap.top().docId == cur.docId ){
				docnode sub = prio_heap.top();
				prio_heap.pop();
				cur.w += sub.w;
				cur.count+=sub.count;
			}
			results.push_back(cur);
		}
		sort(results.begin(),results.end(),compare);
		give_results();
	}
	}
	return 0;
}
