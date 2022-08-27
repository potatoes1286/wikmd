---
layout: default
title: Using the wiki
nav_order: 7
---
# Using the wiki

## Macros

We are slowly trying to integrade a Macro system. For know this only supports a table of concents.

### Table of Contents (TOC)

You can generate a TOC by simply add `[[TOC]]` at the place you'd like the table. It's also possible to specify
the depth by adding a number in the macro. For example:

```
[[ TOC 3 ]]
```

## Latex

It's possible to use latex syntax inside your markdown because the markdown is first converted to latex and after that to html. This means you have a lot more flexibility.

### Change image size

```
![](https://i.ibb.co/Dzp0SfC/download.jpg){width="50%"}
```

### Image references
```
![Nice mountain](https://i.ibb.co/Dzp0SfC/download.jpg){#fig:mountain width="50%"}

Inside picture @fig:mountain you can see a nice mountain.

```

### Math
```
\begin{align}
y(x) &= \int_0^\infty x^{2n} e^{-a x^2}\,dx\\
&= \frac{2n-1}{2a} \int_0^\infty x^{2(n-1)} e^{-a x^2}\,dx\\
&= \frac{(2n-1)!!}{2^{n+1}} \sqrt{\frac{\pi}{a^{2n+1}}}\\
&= \frac{(2n)!}{n! 2^{2n+1}} \sqrt{\frac{\pi}{a^{2n+1}}}
\end{align}
```

```
You can also use $inline$ math to show $a=2$ and $b=8$
```

## Converting the files

Open the wiki folder of your instance.  

|- static  
|- templates  
|- **wiki** <--This folder  
|- wiki.py  

In this folder all the markdownfiles are listed. Editing the files will be visible in the web-version.  

|- homepage.md  
|- How to use the wiki.md  
|- Markdown cheatsheet.md  

The advantage is that u can use the commandline to process some data. For example using pandoc:
```
pandoc -f markdown -t latex homepage.md How\ to\ use\ the\ wiki.md -o file.pdf --pdf-engine=xelatex
```
This creates a nice pdf version of your article.  Its possible you have to create a yml header on top of your document to set the margins etc better
```
---
title: titlepage
author: your name
date: 05-11-2020
geometry: margin=2.5cm
header-includes: |
        \usepackage{caption}
        \usepackage{subcaption}
lof: true
---
```
For more information you have to read the pandoc documentation.

### New features
Create a page with a random id by typing *{id}* in the name.
