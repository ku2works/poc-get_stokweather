## init
source ~/.bashrc
pyenv install --list
pyenv install 3.8.1
pyenv local 3.8.1
pyenv versions

mkdir bin
cd bin
python -m venv python38
source ./bin/python38/bin/activate

## pip update
python -m pip install --upgrade pip --user
pip freeze | Out-File -Encoding UTF8 .\requirements.txt

## package install
pip install --requirement ./requirements-dev.txt
pip install --requirement ./requirements.txt --target ./src/vendor/

## test
python src/functions/stokweather.py

sam validate -t ./deploy/templates/template.yml
sam local invoke StokweatherFunction --region us-west-2 --template ./deploy/templates/template.yml --event ./tests/event_file.json

## deploy
sam package --profile default \
--template-file ./deploy/templates/template.yml \
--s3-bucket repos.sekisuihouse-reit.co.jp \
--s3-prefix stokweather \
--output-template-file ./deploy/out/output.yml

sam deploy --profile default \
--region ap-northeast-1 \
--template-file ./deploy/out/output.yml \
--stack-name stokweather \
--capabilities CAPABILITY_NAMED_IAM \
--parameter-overrides StockweatherCode="xxxx" StockweatherKey="xxxxx"