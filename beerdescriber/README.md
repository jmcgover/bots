# Beer Describer

http://twitter.com/beerdescriber

## Usage

```bash
./make_cbdq.py clean_styles.txt fruit_veg_flavors.txt weight.txt aged.txt flowers_aromatics.txt
```


## Cleanup Rules
- Just move the style to the end
- Anything with a slash is doubled and
	correctly simplified

## Sources
- Beer: https://untappd.com/beer/new_beer
- Flavors: https://northwesternextract.com/flavor-list/
- Aromatics:https://github.com/dariusk/corpora/blob/master/data/foods/herbs_n_spices.json
- Vegetables: https://github.com/dariusk/corpora/blob/master/data/foods/vegetables.json
- Scotches: https://github.com/dariusk/corpora/blob/master/data/foods/scotch_whiskey.json

## Notes

- Line break on HTML tags in vim `:%s/>\s*</>\r</g`
