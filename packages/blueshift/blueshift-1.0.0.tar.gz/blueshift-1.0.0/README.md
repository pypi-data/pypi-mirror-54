# blueshift

Quickly create large amounts of unique serial numbers.  
Forked from [JosephTLyons/andromeda](https://github.com/JosephTLyons/andromeda)

## Installation

Install blueshift with pip: 
```pip install blueshift```

Or, download blueshift [here](https://github.com/mckkaleb/blueshift/archive/0.0.2.tar.gz)

## Usage

To use blueshift in your projects, import it like this:
```python
from blueshift import generate, get_serials #or just 'import blueshift'
```

## Creating Unique Serial Numbers

Using blueshift is very easy and simple. There are only two functions you need to know to start using blueshift. These functions are:
- `generate()`
- `get_serials()`

#### Using generate

Using `generate()` is very simple.

Simply call the `generate()` function
```python
#your code
generate(10, 10) # generate() has two mandatory parameters: number_of_serials, length_of_serials
#more of your code
```
`generate()` takes two mandatory parameters, `number_of_serials` (the number of serials you want to generate) and `length_of_serials` (how many characters you want each to contain), as well as some optional parameters which control which types of character that the serials will contain. The optional parameters are:
- `use_numbers` controls if there will be numbers in the serials
- `use_lowercase` controls if there will be lowercase letters in the serials
- `use_uppercase` controls if there will be uppercase letters in the serials
- `use_symbols` controls if there will be symbols in the serials

For example, if you wanted to have serials that do not contain symbols, then you would call the `generate()` function like this:
```python
generate(10, 10, use_symbols=False)
```
In this example, 10 serials which contained 10 characters would be produced.

#### Using get_serials

`get_serials()` takes no parameters. It only returns the serials created by `generate()`

Example:
```python 
generate(10, 10)
get_serials()
```
In this example, `generate()` was called to create 10 serials with 10 characters in them. Then `get_serials()` was called to return the serials in an array.

## Pitfalls to be Aware of

bluehift does not care if you choose settings that result in a very low pool of
license combinations.  You should be aware of this.  If you run `generate()`
with the following options:

```python
generate(1000, 4, use_uppercase=False, use_lowercase=False, use_symbols=False)
```

the output will be:

```python
['9444', '9474','9494','9464','9484','9434','9424','9404','9414','9454','9244','9274','9294','9264','9284',
'9234', ...]
```

Notice that the licenses are fairly similar.  Also, note that it would be fairly
easy to guess a serial number.  The probability that a random guess would be an
actual serial number is `1000/(10^4) = 0.1`.  It is up to the user to understand
this and adjust the settings to increase the complexity of the output and
decrease the chances of guessing a license number.  Using the example from
earlier with `1000` serial numbers of length `20` using all symbols, the
probability that a random guess would be an actual serial number is
`1000/(62^20) = 1.4196007e-33`.
