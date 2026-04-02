We have used QSAR Model to predict the Level of Toxicity of Compounds with same NR and SR Values.
QSAR Model we calculated the Molecular Descriptors like Toplogical Descriptors, Lipinski Descriptors,
and finally Alert Descriptors to predict the QED Drug Likeness Score .
Then we created an XGBoost Machine Learning Model to classify the compounds using tox21 dataset and then we
further go into QED score
QED score less than 0.3 highly toxic and QED score greater than 0.7 are low toxic compounds.
The tech stack is the three Descriptor CSV files were created and merged using pandas and finally 
classified by XGBoost Classifier which uses Decision trees to predict the outcomes.
Hyper Parameters are tuned to obtain the best accuracy in our Model.
