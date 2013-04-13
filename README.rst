======
dirbot
======

This is a Scrapy project to scrape websites from public web directories.

This project is only meant for educational purposes.

Items
=====

The items scraped by this project are websites, and the item is defined in the
class::

    dirbot.items.Website

See the source code for more details.

Spiders
=======

This project contains one spider called ``dmoz`` that you can see by running::

    scrapy list

Spider: dmoz
------------

The ``dmoz`` spider scrapes the Open Directory Project (dmoz.org), and it's
based on the dmoz spider described in the `Scrapy tutorial`_

This spider doesn't crawl the entire dmoz.org site but only a few pages by
default (defined in the ``start_pages`` attribute). These pages are:

* http://www.dmoz.org/Computers/Programming/Languages/Python/Books/
* http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/

So, if you run the spider regularly (with ``scrapy crawl dmoz``) it will scrape
only those two pages. However, you can scrape any dmoz.org page by passing the
url instead of the spider name. Scrapy internally resolves the spider to use by
looking at the allowed domains of each spider.

For example, to scrape a different URL use::

    scrapy crawl http://www.dmoz.org/Computers/Programming/Languages/Erlang/

You can scrape any URL from dmoz.org using this spider

.. _Scrapy tutorial: http://doc.scrapy.org/intro/tutorial.html 

Pipelines
=========

This project uses a pipeline to filter out websites containing certain
forbidden words in their description. This pipeline is defined in the class::

    dirbot.pipelines.FilterWordsPipeline
