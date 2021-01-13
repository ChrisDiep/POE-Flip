# POE-Flip (WIP)
A site for finding exchange differences between currencies in Path of Exile that can be used to generate short-term profit, i.e. arbitrage for virtual in-game currency. The desired goal is a product that displays viable trades in a visually appealing manner using React/Bootstrap/JavaScript with information provided by a Python Flask back-end.
## Showcase

## Main Libraries
- Flask
- mongoengine
- React
- Bootstrap

## Inner Workings
The algorithm uses Google's OR-tools CP-Sat solver to solve a constraint satisfaction problem made up of systems of equations created from the combinations of listed trades pulled from the Path of Exile API mapped to a graph data structure. A deeper dive into the algorithm can be found below.
### Arbitrage Run-Down
A general break-down of arbitrage and its challenges is provided below to assist in the understanding of a deeper-dive into the algorithm, feel free to skip to the algorithm break-down if this is is not the information you're seeking.

#### Basic 2-Currency Example
With that being said, lets jump straight to a real-world example of arbitrage. We have some amount of dollars and want to buy yen, then sell the yen for dollars and, hopefully, make a profit. This example is a 2 currency mapping, where you go from currency A, to currency B, and back to currency A. Seen in the diagram below, we have two yen sellers: Person 1 selling 1 Dollar for 2 yen with 4 yen total stock, Person 2 selling 1 dollar for 4 yen with 12 yen total stock. Additionally, we have two dollar sellers: person 3 selling 4 dollars for 12 yen with 12 dollars total stock and person 4 selling 3 dollars for 7 yen with 48 dollars total stock.

With the sellers established, we can take a look at whether we can check who we can buy from and sell to that can result in an ending profit. We can see that buying 12 yen from person 2 for 3 dollars and selling to person 3 for 4 dollars, as seen with the black arrow, will result in a dollar profit. This is one possible combination that works with a one to one trade mapping, but what if a single person doesn't have enough stock to sell to a buyer?

<div>
  <img src="https://i.ibb.co/0KRHh7H/Screenshot-869.png" />
</div>

#### M-to-N Relationships
Buying only from person 1 will result in receiving a maximum of 4 yen which is not enough to sell to any of the yen buyers as person 3 and 4 buy 12 yen and 7 yen respectively, therefore we would have to get additional yen by buying from both person 1 and person 2 as seen with the blue arrow. This complicates the arbitrage problem because we would have to check a large combinations of people we could buy from to result in an amount we could sell. In this case we see a 2 to 1 mapping for buying to selling, but this relationship could be a m-to-n relationship with m and n being any integer.

#### Uneven Listings
In addition to having to having to deal with multiple mappings, there would also have to be a check for whether a listing or combination of listings can evenly go into other listings or combination of listings. As seen with the red arrow, we can see that buying 2 yen from person 1 and 4 yen from person 2 results in an amount that does not go evenly into the 7 yen that person 4 desires. In fact, there is no combination of amounts of person 1 and 2 with their respective stock amounts that would result in a possible trade. This further complicates the problem of determining viable arbitrage opportunties as we would have to somehow determine non-viable trades.

#### Additional Currency Trades
In the example above, we have a 2 currency mapping, but, in reality, arbitrage opportunities can come in N currency mappings, where we can traverse multiple currencies to achieve at a final profit. This increases the amount of possible combinations by an extremely large amount. With the example above, we already have 9 possible combinations and thats with 2 currencies and only 4 total trade listings.

<div>
  <img src="https://i.ibb.co/YjT2nPN/Screenshot-870.png" />
</div>

### The Algorithm Break-Down
Given a list of prospective currencies to trade, the library NetworkX is used to create a graph data structure from the information received from the Path of Exile API. This graph is used to generate possible currency combinations given a max amount of currencies for each combination. With the combinations of currencies determined, viable combinations of individual buyer/seller listings for each currency has to be also determined for each combination of currencies.

The problem of determining which combinations of people to buy from and sell to while removing non-viable trade mappings can be solved using constraint programming where we create systems of equations based off of the trade listings for the currencies with the stocks of each person serving as constraints. The algorithm uses this approach of generating systems of equations with constraints to determine the people to buy from and sell to as well as the required trade amounts. A example of an equation created from 10 listings for each currency can be seen in the diagram below. The number of equations is related with the number of currency mappings in a relationship of N-1 equations for a given N integer value of currencies.

<div>
  <img src="https://i.ibb.co/B4KYXrh/Screenshot-871.png" />
</div>
Solving this equation for the 2 currency mapping results in the possible trades seen in the showcase section! With this approach, we have remedied the issues of M-to-N relationships, uneven listings, etc. mentioned in the arbitration summary section, albeit in a way that is rather computation heavy.
