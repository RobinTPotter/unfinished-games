javac -sourcepath src src/DJ.java -d classes
jar cfe DJ.jar DJ -C classes . -C src/resources . 
pause
