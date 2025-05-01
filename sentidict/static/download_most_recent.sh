for FILE in d3.min.js hedotools.min.js jquery.min.js;
do
    wget https://andyreagan.github.io/hedotools/js/$FILE -O $FILE
done
for FILE in hedotools.shift.css
do
    wget https://andyreagan.github.io/hedotools/css/$FILE -O $FILE
done
