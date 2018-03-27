#include<vector>
#include<stdio.h>
#include<sstream>
#include<iostream>
#include <windows.h>
#include<utility>

using namespace std;

class fp_growth{
    private:
        double freq;
        string in;
        string out;
        vector< vector<int> >  transactions;
        int thread = 8;
        int count[8][1000] = {0};
        pair<int,int> range[8];

        static DWORD WINAPI counting_Thread(LPVOID lpParameter);
    public:
        fp_growth(double freq,string in,string out)
        {
            this->freq = freq;
            this->in = in;
            this->out = out;
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
                
            /*
            for(int i=0 ; i < transactions.size() ; i++)
            {
                for(int j=0 ; j < transactions[i].size() ; j++)
                    printf("%d ",transactions[i][j]);
                printf("\n");
            }*/
                
        }
        void fp_build();
        void fp_mining();
        void fp_output();
};

DWORD WINAPI fp_growth::counting_Thread(LPVOID lpParameter)
{
    /*
    first decode the input range
    than start to deal with it
    */
    pair<fp_growth*,int> *te= static_cast< pair<fp_growth*,int>* >(lpParameter);
    
    fp_growth* pt = static_cast<fp_growth *>(te->first);
    int index = te->second;
    
    //printf("???");
    int size;
    for(int i = pt->range[index].first ; i < pt->range[index].second ; i++ )
    {
        printf("i:%d\n",i);
        size = pt->transactions[i].size();
        for(int j=0 ; j<size ; j++)
            pt->count[index][ pt->transactions[i][j] ]++;
    }
    
    //printf("???");

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
        printf("%d ",count[0][i]);
}
void fp_growth::fp_mining()
{

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
    test.fp_mining();
    test.fp_output();
    
    return 0;
}