
.PHONY: clean run

## do not change anything here

all : run

test:
	@javac -d ./src ./src/*.java
	@java -ea -cp ./src functionaldependency.Test ./test.csv 0.8

run:
	@javac -d ./src ./src/*.java
	@java -ea -cp ./src functionaldependency.Run ./data.csv 0.75

clean:
	@rm -rf ./src/functionaldependency
