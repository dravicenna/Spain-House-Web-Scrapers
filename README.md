# Spain-House-Web-Scrapers

 Simple web scrapers using Scrapy to get info from 3 websites

### Installing

You will need to install Scrapy first

```
python -m pip install scrapy
```

Then clone the repo:
```
git clone https://github.com/dravicenna/Spain-House-Web-Scrapers.git
```
And this is all...

## Running

### IDEALISTA parser

```
cd ScrapyIdealistaParcer
scrapy crawl idea_vend
```
OR

```
scrapy crawl idea_alq -s LOG_FILE=idea_alq.log -a tag=lloret
```
To find all properties for rent in Lloret de Mar

## Authors

* **Vitaly Avicenna** - [dravicenna](https://github.com/dravicenna)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

