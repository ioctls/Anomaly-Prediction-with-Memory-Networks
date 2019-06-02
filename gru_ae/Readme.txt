The directory src/ contains all the necessary scripts.
	online_prediction.py is used to predict anomalies by connecting to the broker used for experiments.
	evaluations.py conducts an experiment, for window sizes 2, 5, 7, 10, 12, 15 and 20 on cpu and memory.
	evalutations.py will train, save and evaluate the models needed, and then generate required results.
	report_generation.py will generate the results in results/
	use any as $python3 [file].py

The directory results/
	results.txt containts metrics for all window sizes, evaluated by evaluations.py and report_generation.py
	cpu/ and memory/ contains ROC curves for the mentioned window sizes in evaluations.py

The directory models/
	contains saved models from experiments in evaluations.py and online_prediction.py

The directory data/ contains data collected 44.1hrs normal and 44.3 hrs with falt injections.
