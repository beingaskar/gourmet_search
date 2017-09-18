# Tasty Search: Search Gourmet food reviews.
**Tasty Search** is a search engine built on Python (and Django) to search gourmet food reviews data and return the top K (configurable) reviews that have the highest overlap with input query.

## Dataset
Required dataset is downloaded from [Web data: Amazon Fine Foods reviews](http://snap.stanford.edu/data/web-FineFoods.html)

## Setting up
1. Clone the repo.
2. Create a virtualenv. 
3. Install the requirements.
4. Perform downsampling the data as per requirement. (Eg: to 100,000 entries.)

Use the below management command:

```html
python manage.py perform_downsize --input_file=assets/foods.txt --count=100000
```
* input_file (Mandatory) : File path for gourmet food reviews. (Default value : assets/foods.txt)

* output_file : Output path for downsized file (If path changes required, to be configured in settings as well. Refer **Configurable variables** section below) (Default value : assets/food_reviews.json)
      
* count : Total reviews expected after downsizing. (Default value : 100000)
      
5. Build index of downsized data.

Use the below management command:

```html
python manage.py build_index --input_file=assets/food_reviews.json
```
* input_file (Mandatory) : Path to downsized food reviews file. (Default value : assets/food_reviews.json)

* output_file : Output path for index file. (If path changes required, to be configured in settings as well. Refer **Configurable variables** section below). (Default value : assets/index.json)

6. Run the server the usual way (python manage.py runserver) and you are good to go.

## Configurable variables.

* ASSETS_DIR : The directory where data and index is stored.
* FILES : The location of various assets available.
* MAX_REVIEWS_COUNT_PER_HIT : Maximum number of reviews returned per search. (Defaulted to 20).

## Live Demo
Live demo is deployed on heroku. [Click here](https://gourmet-hunt.herokuapp.com/)

Sample input : cat coffee cinnamon
