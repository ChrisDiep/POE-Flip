# POE-Flip (WIP)
A site for finding exchange differences between currencies in Path of Exile that can be used to generate short-term profit, i.e. arbitrage for virtual in-game currency. Trade listings for each currency are grabbed from the Path of Exile API and the information is mapped out onto a graph data structure. Profitable trades are then determined using constraint programming algorithms. The desired goal is a product that displays viable trades in a visually appealing manner using React/Bootstrap/JavaScript with information provided by a Python Flask back-end.

## Table of Contents

1. [Showcase](#showcase)
1. [Main Libraries](#main-libraries)
1. [Algorithm Explanation](#diving-into-the-algorithm)
1. [Future Steps](#future-steps)

## Showcase
<div>
  <img src="https://i.imgur.com/5Lst6le.gif" />
</div>

#### Currency Display
<div>
  <img src="https://i.imgur.com/OywgbuL.png" width="800"/>
</div>

#### Results Sorted By Profit
<div>
  <img src="https://i.imgur.com/NY0cGO3.png" width="800"/>
</div>

#### Single Result with Whisper Copying
<div>
  <img src="https://i.imgur.com/iGJ5djb.png" width="800"/>
</div>


## Main Libraries
- Flask
- mongoengine
- NetworkX
- Google OR-Tools
- React
- Bootstrap

## Diving into the Algorithm
As an overview, the algorithm uses Google's OR-tools CP-Sat solver to solve a constraint satisfaction problem made up of systems of equations created from the combinations of listed trades pulled from the Path of Exile API mapped to a graph data structure. The determination of these system of equations and the issues this approach tackles are presented below. 

### Arbitrage and its Challenges
A general break-down of arbitrage and its challenges are beneficial to the understanding of a deeper-dive into the algorithm; however, feel free to skip to the [algorithm break-down](#algorithm-break-down) if this is is not the information you're seeking.

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

### Algorithm Break-Down
Given a list of prospective currencies to trade, the library NetworkX is used to create a graph data structure from the information received from the Path of Exile API where nodes store currency information and directed edges between nodes held the trade listings pertaining to those two nodes. This graph is used to generate possible currency combinations given a max amount of currencies for each combination. With the combinations of currencies determined, viable combinations of individual buyer/seller listings for each currency has to be also determined for each combination of currencies.

The problem of determining which combinations of people to buy from and sell to while removing non-viable trade mappings can be solved using constraint programming where we create systems of equations based off of the trade listings for the currencies with the stocks of each person serving as constraints. The algorithm uses this approach of generating systems of equations with constraints to determine the people to buy from and sell to as well as the required trade amounts. A example of an equation created from 10 listings for each currency can be seen in the diagram below. The number of equations is related with the number of currency mappings in a relationship of N-1 equations for a given N integer value of currencies.

<div>
  <img src="https://i.ibb.co/B4KYXrh/Screenshot-871.png" />
</div>

Solving this equation for the 2 currency mapping results in the [possible trades](results-sorted-by-profit) seen in the showcase section! With this approach, we have remedied the issues of M-to-N relationships, uneven listings, etc. mentioned in the arbitration summary section, albeit in a rather computation heavy manner.

## Future Steps

Currently, this site is suitable for usage by a single user; however, due to API limiting concerns and the high comptutation requirements, this would be fairly difficult to host for a large group of users as an increase in the number of users would result in a higher number of API calls and more computations required. While the amount of live data can be limited to a time interval to alleviate these issues, this would be detrimental when the number of users grow larger as users would compete with each other for avaliable listings necessitating smaller intervals between data fetching and computation.

To solve the API limiting issues, in the future, I will be implementing client-side API calls so that the API limits apply per user rather than per instance of the server. Users would be executing API calls through their client and sending this information to the back-end for computation, then receiving the desired information back. With this approach, live data could be refreshed fairly quickly as a single user's client is unlikely to hit the API limit. 

The heavy computation issue can't be remedied without sacrificing some time between live data refreshes, but improvements planned include caching solutions so that computations requested on the same API data set can be obtained from a database if the computation has already been run once. Additionally, this would improve the average user experience as there would be less time spent waiting on the computation to run. 

