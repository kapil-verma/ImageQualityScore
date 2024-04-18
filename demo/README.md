# Optilens

## Demo

- [Item search](https://www.trivago.co.uk/en-GB/srl/hotel-nh-d%C3%BCsseldorf-city?search=100-6365;dr-20240426-20240427;rc-1-2-10)
- [Item search with Optilens Nima](https://www.trivago.co.uk/en-GB/srl/hotel-nh-d%C3%BCsseldorf-city?search=100-6365;dr-20240426-20240427;rc-1-2-10&optilens_nima)
- [Item search with Optilens Gemini](https://www.trivago.co.uk/en-GB/srl/hotel-nh-d%C3%BCsseldorf-city?search=100-6365;dr-20240426-20240427;rc-1-2-10&optilens_gemini)

### Setup

This uses the "Inject Code" Chrome extension, available [here](https://chromewebstore.google.com/detail/inject-code/jpbbdgndcngomphbmplabjginoihkdph).

![Inject setup](img/inject_setup.png).

* Name: `Change hero and gallery image`
* Description: `This changes the hero images for certain items`
* URL Filter: `https://www.trivago.co.uk/*`
* Type: `js`
* Auto Run: `on`
* Code Source: `URL`
* Source URL: `https://raw.githack.com/kapil-verma/ImageQualityScore/colab/demo/inject.js`

The script and the Nima and Gemini data files are served via raw.githack.com to circumvent wrong mime types of the loaded files.