#include<vector>
#include<stdio.h>
#include<sstream>
#include<iostream>
using namespace std;

class fp_growth{
    private:
        double freq;
        string input;
        string output
        vector< vector<int> >  transactions();

    public:
        fp_growth(double freq,string input,string output)
        {
            this.freq = freq;
            this.input = input;
            this.output = output;
        }
        void input()
        {
            freopen(this.input.c_str(),"r", stdin);
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
            }
            */    
        }
        void fp_build()
        void fp_mining();
        void fp_output();
}


void fp_growth::fp_build()
{

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

    fp_growth test(freq,argv[2],argv[3])

    fp_build();
    fp_mining();
    fp_output();
    
    return 0;
}