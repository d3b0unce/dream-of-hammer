# Dream of Hammer

A bullshit avoidance system for the modern internet.

The idea is to evaluate websites based on honesty, simplicity, and quality of content rather than on factors that rely on maximizing ad-revenue, tracking, and annoying SEO tactics. The end goal is to *realize the dream of [Hammer](http://hammer.lol/)*.



## Evaluation factors

Websites can be broadly judged for their quality based on the following factors:

### Visual features

- Good
  - Simplicity
  - Information dense
  - Not many moving parts
- Bad
  - Bloat is undesirable. Bloat can mean:
    - Overuse of style sheets to obscure content / waste screen real-estate
    - Cluttered with distracting elements like popups, chat boxes, newsletter signups
  - Paywalls
  - Components that seek personal information

### Non-visual features

- Good
  - Lean code
  - Fast to load
  - Few network calls
  - Talks to trusted domains
  - Recommended on sites like HN, Lobsters (?)
- Bad
  - Megabytes of JavaScript
  - Tracking and analytics scripts
  - Too many ad units



## Approach

A very high level (very handwavy) approach -

The features described above can be used to assign a score of goodness to a given website. One way is to train a machine-learning model on these features and output a score. To do that, we need a dataset of websites and the ratings/categories people would give them. 

### Making a dataset

To make the process easier, we could learn visual embeddings from screenshots of websites in an unsupervised way (perhaps using an autoencoder)  and cluster websites based on these embeddings. Concatenate the visual embeddings with their corresponding non-visual features to form the final feature vectors. 

If the feature vectors sufficiently capture the information we need, we should find the websites fall into fairly spaced out clusters on running a clustering algorithm. We can then sample websites from these clusters and label them. This is only needed if the size of the training dataset is more than a few thousands.

Use a headless browser to generate screenshots of a fixed size. Also extract as many parameters from the non-visual features section above as possible.

### Making a model

To be able to tell if a website is legit or bullshit, we can train a model; a model that uses both visual and non-visual information related to a website, and assigns it a score of goodness. 

How do we use this model? One way is to use it in a browser extension and show the scores in the search results before the user even open them. If the model is light enough, the predictions can potentially be done within the browser using something like Tensorflow.js. Or we crawl the links on a remote server and cache the results. 



## Goal

From geohot's [Hammer](http://hammer.lol) website

> ### Our mission:
>
> "To organize the world's information and make it accessible to anyone who pays Hammer $30/month"
>
> ### Our motto:
>
> "Don't be evil. And if we ever remove this motto, it's because we are evil now."
>
> ### Our slogan:
>
> "Better search, better results. Hammer"



On a serious note, I think this problem can be solved in a free and open-sourced way.



## Contributing

The idea is at a very nascent stage, as you can tell, and there is no clear path to solving it. The approach I described above is what I think is a good starting point. I foresee a lot of iterations before we have something usable. But we won't know for sure until we write some code and start building it. 

Feel free to create issues, add features, propose ideas!



## Tasks

For the MVP (as the cool kids say), I have the following tasks I am working on. See the [projects](https://github.com/d3b0unce/dream-of-hammer/projects/1) tab for progress:

- [ ] Create a reasonably sized dataset of standardized screenshots of websites and give them a rating [1-10] based on *my impression* of the sites. 

  This is where it gets tricky:

  1. If I do this alone, I infuse my bias into the model.
  2. The websites in the dataset must be representative of the results of any popular search engine. This is a very vague and difficult target, as the quality of results generally depends on the search queries and the search engine.

  My little handspun dataset should be okay for now to build a barebones system. So, I'm considering gathering links from Hacker News and Reddit. The better, eventual way would be to gradually build a crowdsourced dataset. 

- [ ] Train a light-weight CNN model on these images
- [ ] Train an autoencoder and save the embeddings