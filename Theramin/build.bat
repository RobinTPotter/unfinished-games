javac -sourcepath src src/theramin/Theramin.java -d classes
jar cfe Theramin3.jar theramin.Theramin src build.bat -C classes .
pause