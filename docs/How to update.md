<h1>What to do when we want to update our documentation</h1>

```
cd docs
```

***

<h2>When creating a new module:</h2>
```
sphinx-apidoc -o ./source ../src/pipert2
```


<h2>Build the docs</h2>
```
make clean
make html
```


Now all you have to do is to push to master (After CR of course)
