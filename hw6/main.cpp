#include<cstdio>
#include <ctime>
#include<vector>
#include<algorithm>
#include<windows.h>
#include <utility>  
#include <map>
using namespace std;
//simple implement of the Bron–Kerbosch algorithm
/*
BronKerbosch2(R,P,X):
    if P and X are both empty:
        report R as a maximal clique
    choose a pivot vertex u in P ⋃ X
    for each vertex v in P \ N(u):
        BronKerbosch2(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
        P := P \ {v}
        X := X ⋃ {v}
*/
//with eight thread we use mod to decide which
const int thread_num = 8;
clock_t start;
int mimin=2*60+50;

int max_size[thread_num] ={0,0,0,0,0,0,0,0};
vector<int> max_arr[thread_num];


vector< vector<int> > graph;
vector<int> node_count;
vector<int> arr;
bool compare_count (int i,int j){ return (node_count[i] > node_count[j]); }
class set
{
    public:
        vector<int> data;
        map<int,int> mapping;
    
        set()
        {
            data.clear();
            mapping.clear();
        }
        set(set &a)
        {
            this->data = a.data;
            this->mapping = a.mapping;
        }
        bool empty()
        {
            if(this->data.size())
                return false;
            return true;
        }
        bool in(int no)
        {
            if(mapping.find(no) == mapping.end())
                return false;
            return true;
        }
        void join(int no)
        {
            if(mapping.find(no) != mapping.end())
                return ;
            
            int index = data.size();
            data.push_back(no);

            mapping.insert(pair<int,int>(no, index));
        }
        void remove(vector<int> del_arr) //if input is an array make one and remove all 
        {
            vector<int> vec_temp;
            map<int,int> map_temp;

            bool check[82168] = {0};

            for(int i=0;i<this->data.size();i++)
                check[ this->data[i] ] = true;
            
            for(int i=0;i<del_arr.size();i++)
                check[ del_arr[i] ] = false;

            for(int i=0;i<82168;i++)
            {
                if(check[i])
                {
                    map_temp.insert(pair<int,int>(i,vec_temp.size()));
                    vec_temp.push_back(i);
                }
            }

            this->mapping = map_temp;
            this->data = vec_temp;
        }
        void remove(int no)     //if input is int remove it
        {
            if(mapping.find(no) == mapping.end())
                return;
            
            int index = mapping[no];
            mapping.erase(no);

            int last = this->data[ this->data.size()-1 ];
            this->data[index] = last;

            mapping[last] = index;

            this->data.pop_back();
        }
        void intersect(vector<int> check_arr)
        {
            vector<int> vec_temp;
            map<int,int> map_temp;

            bool check[82168] = {0};

            for(int i=0 ; i<this->data.size() ; i++)
                check[ this->data[i] ] = true;
            
            for(int i=0;i<check_arr.size();i++)
                if( check[check_arr[i]] )
                {
                    map_temp.insert(pair<int,int>(check_arr[i],vec_temp.size()));
                    vec_temp.push_back(check_arr[i]);
                }

            this->data = vec_temp;
            this->mapping = map_temp;
        }
        void print()
        {
            for(int i=0 ; i<this->data.size() ; i++)
                printf("%d ",this->data[i]);
            printf("\n");
        }
};

bool BronKerbosch(set &r,set &p,set &x,int index)
{
    for(int i=0 ; i<thread_num ; i++)
        if(r.data.size()+p.data.size() <= max_size[i])
            return false;

    if(p.empty() && x.empty())
    {
        //report R as a maximal clique
        //check if it is largest
        if(r.data.size()>max_size[index])
        {
            double duration = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;
            if(duration>2*60+50)
                return true;

            max_arr[index] = r.data;    
            max_size[index] = r.data.size();
            if(r.data.size()>1200)
                return true;
            //printf("-%d-%d ans:",index,r.data.size());
            //r.print();
        }
    }    
    //choose a pivot vertex u in P ⋃ X
    //find from largest

    bool cc =false;

    int u,i;
    for(i=0 ; i<arr.size() ; i++)
    {
        u = arr[i];
        if ( !(p.in(u) || x.in(u)) )
            continue;
        break;
    }
        
    set temp(p); 
    temp.remove(graph[u]);

    int v,j,z;
    for(j =0 ; j<arr.size() ; j++)
    {
        if(!temp.in(arr[j]))
            continue;
        v = arr[j];
        /*
        for(z=0 ; z<thread_num ; z++)
            if((r.data.size()+1+graph[v].size())<= max_size[z])
            {
                p.remove(v);
                x.join(v);
                continue;
            }
        */
        set temp_r(r);
        temp_r.join(v);
        set temp_p(p);
        temp_p.intersect(graph[v]);
        set temp_x(x); 
        temp_x.intersect(graph[v]);
        
        cc = BronKerbosch( temp_r , temp_p  , temp_x ,index);
        if(cc)
            return true;
        p.remove(v);
        x.join(v);
    }
    return false;
}



DWORD WINAPI counting_Thread(LPVOID lpParameter)
{
    /*
    first decode the input range
    than start to deal with it
    */
    int *now= static_cast< int* >(lpParameter);
    int i,j;

    //printf("----%d\n",*now);
    set r;
    set p;
    set x;

    for(i=0;i<arr.size();i++)
        if(graph[ arr[i] ].size())
            p.join(arr[i]);
    

    for(i=0 ; i<arr.size() ; i++)
    {
        if(i%thread_num == *now)
        {
            /*
            printf("new round-%d--",*now);
            x.print();
            */
            r.join(arr[i]);
            p.remove(arr[i]);

            set temp_p(p);
            temp_p.intersect(graph[arr[i]]);
            set temp_x(x); 
            temp_x.intersect(graph[arr[i]]);

            BronKerbosch(r,temp_p,temp_x,*now);
            x.join(arr[i]);    
            r.remove(arr[i]);
        }
        else
        {
            p.remove(arr[i]);
            x.join(arr[i]);    
        }
    }
    return 0;
}

void find(char *output_file)
{
    for(int i=0;i<thread_num;i++)
    {
        max_size[i] = 0;
        max_arr[i].clear();
    }
    set r;
    set p;
    set x;

    for(int i=0;i<graph.size();i++)
        if(graph[i].size())
            p.join(i);
    int index=0;

    //in this place we should part the data in to eight part 
    HANDLE myHandle[thread_num];
    DWORD myThreadID[thread_num];
    int now[thread_num];

    //create thread for counting
    for(int i=0 ; i<thread_num ; i++)
    {
        now[i] = i;
        myHandle[i] = CreateThread(0, 0,counting_Thread, &now[i], 0, &myThreadID[i]);
    }
    for(int i=0 ; i<thread_num ; i++)
    {
        int dur = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;
        //printf("dur:%d\n",dur);
        if(mimin<dur)
            break;
        WaitForSingleObject(myHandle[i],(mimin-dur)*1000);
    }    
    
    double duration = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;

    printf("duration:%lf\n",duration);
    
    int mm=0;
    for(int i=1;i<8;i++)
        if(max_size[mm]<max_size[i])
            mm=i;

    sort(max_arr[mm].begin(),max_arr[mm].end());
    FILE *out =fopen(output_file,"w");
    for(int i=0;i<max_arr[mm].size();i++)
        fprintf(out,"%d\n",max_arr[mm][i]);
}




int main(int argc,char *argv[])
{
    FILE * in = fopen(argv[1],"r");    
    int q,p;
    start = std::clock();
    
    //
    while(1)
    {
        fscanf(in,"%d %d",&q,&p);
        if(feof(in))
            break;
        while((p+1)>graph.size() )
            graph.push_back(vector<int>());
        
        while((p+1)>node_count.size() )
            node_count.push_back(0);
        
        node_count[q]++;
        node_count[p]++;

        graph[q].push_back(p);
        graph[p].push_back(q);
    }
    fclose(in);

    for(int i=0;i<node_count.size();i++)
        arr.push_back(i);
    sort(arr.begin(),arr.end(),compare_count );
    find(argv[2]);
    return 0;
}