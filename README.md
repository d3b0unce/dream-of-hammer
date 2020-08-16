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

A very high level (very handwavy) approach that could work is -

### Making a dataset

We could use the features described above to assign a score of goodness to websites. One way would be to have a machine learning model that can learn from these features. However, we would need a dataset of websites and ratings/categories humans would assign them. To make the process easier, we could learn visual embeddings from screenshots of websites in an unsupervised way (perhaps using an autoencoder)  and cluster websites based on these embeddings. Concatenate these embeddings with the corresponding non-visual features described above to form a final feature vector per website. If these feature vectors sufficiently capture the information seek, we should be seeing the websites fall into nice clusters on running a clustering algorithm. We could then sample websites from these clusters and label them.

### Making a model

A convenient way to use this system is to have a browser extension that can evaluate the websites one visits. The predictions can be either done within the browser using a lightweight Tensorflow.js model, or on a remote server. 



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

