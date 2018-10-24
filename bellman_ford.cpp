#include<iostream>
#include<list>
#include<stack>
#include<bits/stdc++.h>

using namespace std;

void bellman_ford(int dist[],int edges[][3],int E,int N)
{ int start,end,weight;
	for (int i=0;i<E;i++)
	{
		start = edges[i][0];end=edges[i][1];weight=edges[i][2];
		if(dist[end]>dist[start]+weight)
		{
			dist[end]=dist[start]+weight;
		}
	}
}

bool is_negative_cycle(int dist[],int edges[][3],int E,int N)
{int start,end,weight;
	for (int i=0;i<E;i++)
	{
		start = edges[i][0];end=edges[i][1];weight=edges[i][2];
		if(dist[end]>dist[start]+weight)
		{
			return true;
		}
	}
	return false;
}

int main()
{
	int N,E;
	cin>>N>>E;
	int edges[E][3];
	for(int i=0;i<E;i++)
	{
		cin>>edges[i][0]>>edges[i][1]>>edges[i][2];
	}
	int dist[N];
	for(int i=0;i<N;i++)
	{
		if(i==0) dist[i]=0;
		else dist[i]=INT_MAX;
	}
	bellman_ford(dist,edges,E,N);
	if(is_negative_cycle(dist,edges,E,N))cout<<"cycle_exists";
	else cout<<"no_cycle";
	return 0;
}