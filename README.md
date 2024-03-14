Haematopoietic stem cell transplantation outcomes predictor
=========================================================

The model predicts the risk for 5 events: EFS, death, GVHD, rejection, and relapse after one year from hematopoietic stem cell transplantation and the percentile.
The model is available as a web application and can be predicted directly through the website. 

The code is available in the repository and can be run locally as well, with web front end or command line.

You need to provide the model with an input file named input_efs.csv.
The file should be with the fields like in the file input_example/input_efs_with_default_values.csv. 
The fields are the first line in the file and the values are the second line in the file.
You should fill in the values with your data.
The file "input_example/efsdict annotated.csv" is the dictionary of the fields in the input file. 
The column "Variable" is the name of the field in the input file, the column "Description" is the description of the field, the column "Type" is the type of the field, the column "Value" is the values options you can fill as value, and the column "Lable" is the description of each value.
For Categorical fields, you should fill in the value that fits your label.
For Continuous fields, you should fill the value as it is.
For one-hot fields, you should fill 1 in the field called the filed name with the value you want to fill, and 0 in the other fields.

After you fill in the input file and save it in the directory "EFS/app", you can run -
python predict.py
The result will be in the file "efs_res.json" in the directory "EFS/app".
