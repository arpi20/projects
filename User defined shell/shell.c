#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include<string.h>
#include<errno.h>
#include<sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>
#include <wait.h>
int ha=0,pr=0;
int j;
int pp=0,bb=0,cc=0;
int pidval[200],pbground[200],pcurr[200];
char cmnd[100][20];
char bground[100][20];
char curr[100][20];
void sig_handler(int signum){
	if(signum == 2 || signum == 20){
	ha=1;
	}
	signal(SIGINT, sig_handler);
	signal(SIGTSTP, sig_handler);
	return;
}

void child_handler(int signum){
	int pid;
	pid = waitpid(WAIT_ANY, NULL, WNOHANG);
	for(j=0;j<bb;j++)
	{if (pbground[j]==pid)
	{if(pid > 0){
		printf("%s %d exitted normally\n",bground[j],pbground[j]);
                ha=1;
		strcpy(curr[cc],bground[j]);
		pcurr[cc++]=pbground[j];
	}
	}
	}
	signal(SIGCHLD, child_handler);
	return;
}
int execute_only_pipes(char *);
int main(int argc, char *argv[], char *envp[])
{    
	signal(SIGINT,  sig_handler);
	signal(SIGTSTP, sig_handler);
	signal(SIGCHLD,SIG_IGN);
	signal(SIGCHLD, child_handler);
	char c = '\0';
	pid_t pid,pid1;
	char *path;
char *user;
	char sys[1024];
	sys[102]='\0';
	gethostname(sys,102);
char *q,*p,*r;
	p=(char*)malloc(sizeof(char)*100);
	r=(char*)malloc(sizeof(char)*50);
	q=(char*)malloc(sizeof(char)*50);
//	pids st[100];
	int flag=0,flagp=0;
	int a=0;
	char *get_current_dir_name(void);
	path=get_current_dir_name();
	strcat(p,path);
	user=getlogin();
	char s[100];
	char ss[100];
	 int t=0;
	int h=0,i,j;
	char *p1;
	char *aut;
	char all[100][100];
	char history[100][100];
	char *command[20];
	aut=(char *)malloc(sizeof(char)*50);
	printf("\n<%s@%s:~> ",user,sys);
	s[0]='\0';
	while(c != EOF) {
//	printf("o\n");
		if (flag==0 && ha==0)
		{c = getchar();}
	else if(ha==1){
		ha=0;
		continue;}
		if(c!='\n' && flag==0)
		{strncat(s,&c,1);
		}
		else
		{
		if (s[0]=='\0')
		{
				printf("\n<%s@%s~%s> ",user,sys,q);
		continue;}
		strcpy(history[h],s);
		h++; 
		        a=0;
			p1=NULL;
			strcpy(ss,s);
			p1=strtok(s,"	 ");
			while(p1!=NULL)
			{
			command[a++]=p1;
			p1=strtok(NULL," 	");
			}
			command[a] = (char *)NULL;
			//for(i=0;i<a;i++)
                         // {printf("%s\n",command[i]);}

				if (strcmp(command[0],"cd")==0)
				{      
					if(command[1]==(char*)NULL){
					chdir(p);
					q=&p[strlen(p)];
					}
					else{
					path[0]='\0';  
					chdir(command[1]);
					path=get_current_dir_name();
					q=&path[strlen(p)];
					
					}
				}

				else if(strcmp(command[0],"quit")==0)
				{exit(0);}
				else if(strcmp(command[0],"hist")==0 && command[1]==NULL)
                                {    for(i=0;i<h;i++)
				{printf("%d. %s\n",i+1,history[i]);}
				}

				else if(strstr(command[0],"!hist")!=NULL)
				{r=&command[0][5];
				j=atoi(r);
				s[0]='\0';
				strcpy(s,history[j-1]);
				flag=1;
				continue;
				}
				else if(strstr(command[0],"hist")!=NULL)
				{
				r=&command[0][4];
				j=atoi(r);
				for(i=h-j-1;i<h-1;i++)
				{printf("%d. %s\n",(i-(h-j)+2),history[i]);}
				}

				else if(strcmp(command[0],"pid")==0 && command[1]==NULL)
				{
					printf("commandname:./a.out processid:%d\n",getpid());
				}

				else if(strcmp(command[0],"pid")==0 && strcmp(command[1],"all")==0)
                                {
                                for(i=0;i<pp;i++)
				{printf("command name:%s process id : %d\n",cmnd[i],pidval[i]);}
                                
				}

				else if(strcmp(command[0],"pid")==0 && strcmp(command[1],"current")==0)
				{
				for(i=0;i<cc;i++)
				{printf("command name:%s process id : %d\n",curr[i],pcurr[i]);}
				}
			/*	else if(command[1]!=NULL && strcmp(command[1],"&")==0)
				{strcat(aut,command[0]);
					strcpy(all[t],command[0]);
					t++;
					pid=fork();
					if(pid==0)
					{pid1=fork();
					if (pid1==0)
					{execlp(aut,command[0],NULL);}
					else
					{
						exit(0);
						}
						}
						else
						{wait(NULL);}

						}
			 */

				else if(command[1]!=NULL && strcmp(command[1],"&")==0)
				{pid=fork();
					if(pid==0)
					{execvp(command[0],command);}
					else
					{
					strcpy(bground[bb],command[0]);
					pbground[bb++]=pid;
					printf("command %s pid %d\n",command[0],pid); 
					}
					*command=(char *)NULL;
					a=0;
				}
				else
				{
				execute_only_pipes(&ss[0]);
				*command=(char*)NULL;
			//	printf("pid val=%d\n",pidval[0]);
				}

				flag=0;
				if(flagp==0)
				{printf("\n<%s@%s~%s> ",user,sys,q);}
				else
				{flagp=0;}
				s[0]='\0';
				a=0;

	}
	}
	return 0;
}


int execute_only_pipes(char* buffer)
{
	char *temp = NULL, *pipeCommands[100], *cmdArgs[10],pipeComm[100];
	int newPipe[2], oldPipe[2], pipesCount, aCount, i, status,in,out,store,store1;
	pid_t pid;

	pipesCount = 0; /* This variable will contain how many pipes the command contains */

	/* Counting the number of pipes and splitting them into pipeCommands */
	temp = strtok(buffer,"|");
	while(temp!=NULL)
	{
		pipeCommands[pipesCount++] = temp;
		temp = strtok(NULL, "|");
	}   
	pipeCommands[pipesCount] = (char*)NULL;
	//      cmdArgs[++pipesCount] = NULL;
	for(i = 0; i < pipesCount; i++)  
	{    
		temp=NULL;
		aCount = 0;
		pipeComm[0]='\0';
		strcpy(pipeComm,pipeCommands[i]);
		temp=strtok(pipeCommands[i]," ");
		while(temp!=NULL)
		{
			if(strcmp(temp,"<")==0)
			{       fflush(stdin);
			        store1=dup(0); 
				temp=strtok(NULL," ");
				in=open(temp,O_RDONLY);
				cmdArgs[aCount++]=temp;
				dup2(in,0);
				close(in);
			}
			else if(strcmp(temp,">")==0)
			{
				fflush(stdout);
				store=dup(1);//stores stdout in variable temporarily
				temp=strtok(NULL," ");
				out=open(temp,O_WRONLY | O_TRUNC | O_CREAT, S_IRUSR | S_IRGRP | S_IWGRP | S_IWUSR);
				dup2(out,1);
			 //temp = strtok(NULL," ");
				close(out);
			}
			else
			{    cmdArgs[aCount++] = temp;}
			temp=strtok(NULL," ");
		}

		cmdArgs[aCount] = (char*)NULL;


		/* If there still are commands to be executed */
		if(i < pipesCount-1)
		{
			pipe(newPipe); //create a pipe
		}

		pid = fork();

		if(pid == 0)  /* Child */
		{
			/* If there is a previous command */
			if(i > 0)
			{
				close(oldPipe[1]);
				dup2(oldPipe[0], 0);
				close(oldPipe[0]);
			}

			/* If there still are commands to be executed */
			if(i < pipesCount-1)
			{
				close(newPipe[0]);
				dup2(newPipe[1], 1);
				close(newPipe[1]);
			}
			/* Execute it */

			int res = execvp(cmdArgs[0], cmdArgs);
			if (res == -1)
			{
				printf("Error. Command not found: %s\n", cmdArgs[0]);
				//fflush(stdout);
			exit(1);
			}
			//else printf("executed!\n");
			//exit(1);
		}
		else /* Father */
		{       
			/* If there is a previous command */
			if(i > 0)
			{
				close(oldPipe[0]);
				close(oldPipe[1]);
			}

			/* do we have a next command? */
			if(i < pipesCount-1)
			{
				oldPipe[0] = newPipe[0];
				oldPipe[1] = newPipe[1];
			}
			if(i == pipesCount-1)
			{
				waitpid(pid, &status, 0);
			}
			fflush(stdin);
			dup2(store1,0);
			fflush(stdout);
			dup2(store,1);
			pidval[pp]=pid;
			strcpy(cmnd[pp++],pipeComm);
		}
	}
}


