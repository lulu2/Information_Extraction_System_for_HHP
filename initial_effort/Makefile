output = thereItIs.txt
input = record.txt

all:
	python preprocess.py $(input) filtered.txt
	java -Xmx512m -jar ollie-app-latest.jar filtered.txt --split > output.txt
	python loadOutput.py output.txt $(output)

clean:
	rm output.txt filtered.txt