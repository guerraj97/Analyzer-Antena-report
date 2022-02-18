FROM  continuumio/anaconda3

ENV /Users/jguerra/Documents/GitHub/Analyzer-Antena-report /app
WORKDIR /Users/jguerra/Documents/GitHub/Analyzer-Antena-report
COPY . /Users/jguerra/Documents/GitHub/Analyzer-Antena-report

COPY requirements.txt requirements.txt

#---------------- Prepare the envirennment
RUN conda update --name base conda &&\
    conda env create --file environment.yaml

SHELL ["conda", "run", "--name", "app", "/bin/bash", "-c"]

RUN pip install -r requirements.txt
VOLUME /Users/jguerra/Documents/GitHub/Analyzer-Antena-report/csv/

#ENTRYPOINT ["conda", "run", "--name", "app", "python", "Report_Generator_CLI.py"]
# /Users/jguerra/Documents/GitHub/Analyzer-Antena-report/csv/GAIN_12DEG_PAD_B.csv