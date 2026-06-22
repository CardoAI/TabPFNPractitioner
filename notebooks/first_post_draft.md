I have spent years as a practitioner working with tabular data, building mostly tree-based models and the usual general-purpose models for tables. As most of you know, the last few months have brought something of a revolution here: the arrival of tabular foundation models.

The ones I keep coming back to are the in-context learning models, mainly TabPFN and TabICL, which now sit at the top of the latest benchmarks.

And yet almost all of the conversation so far has been about performance, and sometimes about the theory of how that performance was achieved. As a data scientist, that is not the part I am most curious about. What I really want to know is simpler and more practical: how does my model building change when I work with these models, and with TabPFN in particular?

I felt there was a gap there. So I decided to deep dive into how this model actually works, and how it handles the things that really show up in a dataset:

- Missing values
- High-cardinality and categorical variables
- Skewed variables
- Correlated variables
- Feature engineering
- The bias-variance trade-off

My hope is that this helps other practitioners build a feel for how the model behaves, and for the strategies that actually work when you bring TabPFN to a new problem.
