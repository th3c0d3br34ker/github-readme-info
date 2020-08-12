FROM nikolaik/python-nodejs:latest

# Install dependencies.
ADD requirements.txt /requirements.txt
ADD GenerateREADME.py /GenerateREADME.py
ADD utility.py /utility.py
RUN pip install -r requirements.txt

ENV NPM_CONFIG_PREFIX=/home/node/.npm-global

RUN npm -g config set user root

RUN npm install -g vega-lite vega-cli canvas

# Run the file
ENTRYPOINT ["python", "/GenerateREADME.py"]