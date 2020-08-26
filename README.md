# Extract Faces processing block

An example custom processing block for [Edge Impulse](https://www.edgeimpulse.com). The original template can be found here: https://github.com/edgeimpulse/example-custom-processing-block-python

### To build:

```
docker build -t extract-faces-block .
```

### To run:

```
docker run -p 1212:1212 -it --rm extract-faces-block
```

Use [ngrok](https://ngrok.com) to make the port accessible to the studio.

In the Studio: Create Impulse > Add a processing block > Add custom block. Paste the `https` ngrok URL.