rm -r tmp
mkdir tmp
cat ./selected/*.csv > tmp/raw_dataset.csv
cat tmp/raw_dataset.csv | uniq > tmp/raw_dataset_uniq.csv
cut -d ',' -f 1 tmp/raw_dataset_uniq.csv > tmp/X_train.txt
cut -d ',' -f 2 tmp/raw_dataset_uniq.csv > tmp/y_train.txt
cat tmp/X_train.txt | gsed 's/[-,]//g' | tr '[:upper:]' '[:lower:]'  > tmp/X_train_lowercase.txt
mkdir tmp/output
paste -d ',' tmp/X_train_lowercase.txt tmp/y_train.txt > tmp/output/dataset.csv
echo -e "\"NAME\",\"NATIONALITY\"\n$(cat tmp/output/dataset.csv)" > tmp/output/dataset.csv
echo "number of classes: "
cut -d ',' -f 2 tmp/output/dataset.csv | uniq | wc -l
cp tmp/output/dataset.csv ../../data