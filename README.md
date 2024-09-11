# DC2

This program is created to demonstrate capabilities what can be achieved in DevOps space using 
generative AI.

###The story
1. A chat interface with DC2 will be opened.
2. User will request DC2 to transform an application from Java to Python. As input, user will provide
a code repository of the java application. The code repository contains,
   1. Application code
   2. Working pipeline code for Java
      - code checkout
      - sonarqube analysis 
      - build
      - docker image creation
      - push to docker registry
      - deploy
      - run functional test
      - generate functional test report
   3. Docker file
   4. Working functional test code
3. DC2 will take the input and convert the code into python code.
4. DC2 will create respective repository, pipeline, test cases
5. User use the newly created setup and perform a change in the python code to run the pipeline and
generate functional test report

---



The chat bot UI is developed to be hosted in NGINX. The folder "site-content" is the folder which will be mapped to 
/usr/share/nginx/html and the web server is mapped to port 8080. The command is
```
$ docker run -it --rm -d -p 8080:80 --name web -v ~/lab/DC2/site-content:/usr/share/nginx/html nginx
```

to run ollama package
docker run -d -v /Users/abhijitdas/lab/DC2/ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

In the ollama exec execute
ollama run llama3
or execute 
docker exec -it ollama ollama run llama3
it will download the 4.7 gb model
---------------------------------------------
To generate requirements.txt file with the dependencies of current project
```
$ pip freeze > requirements.txt
```
To install all the packages written in requirements.txt file
```
$ pip install -r requirements.txt
``` 
 