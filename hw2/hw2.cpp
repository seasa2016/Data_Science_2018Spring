#include<vector>
#include<stdio.h>
#include<sstream>
#include<iostream>
#include<windows.h>
#include<utility>
#include<algorithm>
#include<map>
#include<queue>

using namespace std;
int compare_value[1000];

class fp_growth{
    private:
        double freq;
        string in;
        string out;
        vector< vector<int> >  transactions;
        int thread = 8;
        int count[8][1000] = {0};
        pair<int,int> range[8];

        int rule[1000]={0};

        static DWORD WINAPI counting_Thread(LPVOID lpParameter);
        static DWORD WINAPI sorting_Thread(LPVOID lpParameter);
        static DWORD WINAPI making_tree_Thread(LPVOID lpParameter);

        struct tree_node{
            int time;
            int value;
            map< int , tree_node*> child;
            tree_node* next = NULL;
            tree_node* back = NULL;
            
            bool check = false;
            tree_node* up = NULL;
        }*root; //root of the fp tree

        tree_node* (find_root[8][1000]) = {0};

    public:
        void print_tree(int index)
        {
            queue< tree_node* > parser;
            tree_node * tree_root;

            for(int i=index ; i<1000 ; i+=8)
            {        
                tree_root = &this->root[i];
                parser.push(tree_root);

                while(!parser.empty())
                {
                    tree_root = parser.front();
                    parser.pop();
                    printf("%d  ",tree_root->value);
                    
                    for(pair< int , tree_node* > temp : tree_root->child)
                    {
                        parser.push(temp.second);
                    }
                }
                printf("\n");
            }
            
        }
        fp_growth(double freq,string in,string out)
        {
            this->freq = freq;
            this->in = in;
            this->out = out;
            root = new tree_node[1000];
        }
        void print()
        {
            for(int i=0 ; i < transactions.size() ; i++)
            {
                for(int j=0 ; j < transactions[i].size() ; j++)
                    printf("%d ",transactions[i][j]);
                printf("\n");
            }
        }
        void input()
        {
            
            freopen(this->in.c_str(),"r", stdin);
            string line;
            //read until EOF
            
            while(!getline(cin, line).eof())
            {
                vector<int> arr;
                istringstream ssline(line);
                
                string number;
                while(getline(ssline, number, ','))
                    arr.push_back(atoi(number.c_str()));
                
                transactions.push_back(arr);
            }
        }
        void fp_build();
        void fp_mining();
        void fp_output();
};

DWORD WINAPI fp_growth::mining_Thread(LPVOID lpParameter)
{
    /*
    first decode the input range
    than start to deal with it
    */
    pair<fp_growth*,int> *te= static_cast< pair<fp_growth*,int>* >(lpParameter);
    
    fp_growth* pt = static_cast<fp_growth *>(te->first);
    int index = te->second;
    
    tree_node *temp;

    for(int i=999 ; i>=0 ; i--)
    {
        if( pt->find_root[index][i] != NULL)
        {
            temp = pt->find_root[index][i];

            if(temp->check == false)    
            {
                /*
                find to the top and collect all the combination
                */

            }

            temp = temp->next;
        }
    }


    return 0;
}

DWORD WINAPI fp_growth::counting_Thread(LPVOID lpParameter)
{
    /*
    first decode the input range
    than start to deal with it
    */
    pair<fp_growth*,int> *te= static_cast< pair<fp_growth*,int>* >(lpParameter);
    
    fp_growth* pt = static_cast<fp_growth *>(te->first);
    int index = te->second;
    
    int size;
    for(int i = pt->range[index].first ; i < pt->range[index].second ; i++ )
    {
        size = pt->transactions[i].size();
        for(int j=0 ; j<size ; j++)
            pt->count[index][ pt->transactions[i][j] ]++;
    }
    return 0;
}

int compare(int i,int j)
{
    if(compare_value[i] != compare_value[j])
        return compare_value[i] > compare_value[j];
    return i>j;
}

DWORD WINAPI fp_growth::sorting_Thread(LPVOID lpParameter)
{ 
    /*
    first decode the input range
    than start to deal with it
    */
    pair<fp_growth*,int> *te= static_cast< pair<fp_growth*,int>* >(lpParameter);
    
    fp_growth* pt = static_cast<fp_growth *>(te->first);
    int index = te->second;
    
    int size;
    for(int i = pt->range[index].first ; i < pt->range[index].second ; i++ )
        sort(pt->transactions[i].begin(),pt->transactions[i].end(),compare);
    
    return 0;
}

DWORD WINAPI fp_growth::making_tree_Thread(LPVOID lpParameter)
{
    /*
    first decode the input range
    than start to deal with it
    */
    pair<fp_growth*,int> *te= static_cast< pair<fp_growth*,int>* >(lpParameter);
    
    fp_growth* pt = static_cast<fp_growth *>(te->first);
    int index = te->second;
    
    //use the random idea, we should be able to use mod to get eight same size part
    int size = pt->transactions.size();
    int ssize;

    tree_node *tree_root;
    for(int i=0 ; i<size ; i++)
    {
        if(pt->transactions[i][0] % pt->thread == index)
        {
            //printf("%d  ",pt->transactions[i][0]);
            tree_root = &pt->root[ pt->transactions[i][0] ];
            tree_root->time++;
            tree_root->value = pt->transactions[i][0];
            tree_root->up = NULL;

            if( pt->find_root[index][ pt->transactions[i][0] ] == NULL )
            {
                tree_root->next = pt->find_root[index][ pt->transactions[i][0] ];
                tree_root->back = NULL;
                pt->find_root[index][ pt->transactions[i][0] ] = tree_root;
            }
            else
            {
                tree_root->next = pt->find_root[index][ pt->transactions[i][0] ] ;
                tree_root->back = pt->find_root[index][ pt->transactions[i][0] ]->back ;
                pt->find_root[index][ pt->transactions[i][0] ]->back = tree_root ;
                pt->find_root[index][ pt->transactions[i][0] ] = tree_root;
            }

            ssize = pt->transactions[i].size();
            for(int j=1 ; j<ssize ; j++)
            {
                //printf("%d  ",pt->transactions[i][j]);

                if( tree_root->child[ pt->transactions[i][j] ] == NULL )
                {
                    tree_root->child[ pt->transactions[i][j] ] = new tree_node;
                    tree_root->child[ pt->transactions[i][j] ]->up = tree_root;

                    tree_root = tree_root->child[ pt->transactions[i][j] ];
                    tree_root->value = pt->transactions[i][j]; 
                    
                    if( pt->find_root[index][ pt->transactions[i][j] ] == NULL )
                    {
                        tree_root->next = pt->find_root[index][ pt->transactions[i][j] ];
                        tree_root->back = NULL;
                        pt->find_root[index][ pt->transactions[i][j] ] = tree_root;
                    }
                    else
                    {
                        tree_root->next = pt->find_root[index][ pt->transactions[i][j] ] ;
                        tree_root->back = pt->find_root[index][ pt->transactions[i][j] ]->back ;
                        pt->find_root[index][ pt->transactions[i][j] ]->back = tree_root ;
                        pt->find_root[index][ pt->transactions[i][j] ] = tree_root;
                    }
                }
                else
                {
                    tree_root = tree_root->child[ pt->transactions[i][j] ];    
                }

                tree_root->time++;
            }
            //printf("\n");
        }
    }
    

    return 0;
}


void fp_growth::fp_build()               
{
    //in this place we should part the data in to eight part 
    int size = this->transactions.size();
    int dis = this->transactions.size() / 8;
    int index;
    HANDLE myHandle[8];
    DWORD myThreadID[8];

    pair<fp_growth*,int >para[8];

    
    //create thread for counting
    for(int i=0 ; i<8 ; i++)
    {
        this->range[i].first = i * dis;
        this->range[i].second = (i+1) * dis;
        if(i==7)
            this->range[i].second = this->transactions.size();
        
        para[i].first = this;
        para[i].second = i;

        myHandle[i] = CreateThread(0, 0, fp_growth::counting_Thread, &para[i], 0, &myThreadID[i]);
    }
    for(int i=0 ; i<8 ; i++)
        WaitForSingleObject(myHandle[i],INFINITE);
   
    for(int i=1;i<8;i++)
        for(int j=0;j<1000;j++)
            count[0][j] += count[i][j];

    for(int i=0;i<1000;i++)
    {
        compare_value[i] = count[0][i];
        //printf("%d ",compare_value[i]);
    }     
    printf("\n");

    for(int i=0 ; i<8 ; i++)
        myHandle[i] = CreateThread(0, 0, fp_growth::sorting_Thread, &para[i], 0, &myThreadID[i]);
    for(int i=0 ; i<8 ; i++)
        WaitForSingleObject(myHandle[i],INFINITE);
   
    //this->print();


    //finfish of sorting so its time to make the tree
    for(int i=0 ; i<8 ; i++)
        myHandle[i] = CreateThread(0, 0, fp_growth::making_tree_Thread, &para[i], 0, &myThreadID[i]);
    for(int i=0 ; i<8 ; i++)
        WaitForSingleObject(myHandle[i],INFINITE);
    
    for(int i=0;i<1000;i++)
        this->rule[i] = i;
    sort(this->rule,this->rule+1000,compare);

    /*
    for(int i=0;i<1000;i++)
        printf("%d ",this->rule[i]);
    printf("\n");*/
}
void fp_growth::fp_mining()
{
    for(int i=0 ; i<8 ; i++)
        myHandle[i] = CreateThread(0, 0, fp_growth::mining_Thread, &para[i], 0, &myThreadID[i]);
    for(int i=0 ; i<8 ; i++)
        WaitForSingleObject(myHandle[i],INFINITE);
}
void fp_growth::fp_output()
{

}

int main(int argc,char *argv[])
{
    if(argc != 4)
    {
        fprintf(stderr,"there should be 4 command line input\n");
        return 0;
    }
    double freq;
    if(sscanf(argv[1],"%lf",&freq) == 0)
    {
        fprintf(stderr,"the first input should be number\n");
        return 0;    
    }

    fp_growth test(freq,argv[2],argv[3]);

    test.input();

    test.fp_build();
    //test.fp_mining();
    //test.fp_output();
    
    return 0;
}