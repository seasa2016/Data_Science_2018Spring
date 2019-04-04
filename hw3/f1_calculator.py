from sklearn.metrics import f1_score
from  sklearn.datasets import load_svmlight_file

f = open('./TestSample_HW3/output_dataset3')

text = f.read()

text = text.split()
text = [ int(_) for _ in text]
print(len(text))
x,y = load_svmlight_file('./TestSample_HW3/dataset3_sample_val_out.txt')

print(y.shape)

print(f1_score(y, text, average='micro')  )