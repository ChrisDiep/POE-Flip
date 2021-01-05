import React from 'react';
import { Container, Row, Col, Image } from 'react-bootstrap';

function ListingHeader({ tradeInfo, imagesRef }) {
  const currencies = tradeInfo['trades'];
  const listings = tradeInfo['listings'];
  const listingsCurr = Object.keys(listings)
  const whispers = [];
  const amt = {};
  //Iterates through currency
  for (let index = 0; index < currencies.length; index += 1) {
    if (index === 0) {
      amt["startCurr"] = 0;
      for (let j = 0; j < listings[currencies[1]].length; j += 1) {
        amt["startCurr"] += listings[currencies[1]][j]["info"]["want"]["min_amount"] * listings[currencies[1]][j]["order_size"];
      }
    } else {
      amt[currencies[index]] = 0;
      for (let j =0; j < listings[currencies[index]].length; j += 1) {
          whispers.push(listings[currencies[index]][j])
          amt[currencies[index]] += listings[currencies[index]][j]["order_size"] * listings[currencies[index]][j]["info"]["has"]["min_amount"]
      }
    }
  }
console.log(amt)
return (
  <Container style={{ "display": "flex", "align-items": "center" }}>
    <Col xl={3} style={{ "text-align": "left" }}>
      <div>{`Total Profit: ${tradeInfo['total_profit']}`}</div>
      <div>{`Profit per Trade: ${tradeInfo['profit_per_trade']}`}</div>
    </Col>
    <Col xl={7}>
      {currencies.map((currency, index) => {
        console.log(`Index: ${index} Whisper: ${whispers[index]}`)
        const firstOrLast = index === 0 || index === currencies.length - 1;
        return (
          <div style={{ "display": "inline" }}>
            {index !== 0 &&
              <span className={'fa fa-arrow-right m-2'}></span>}
            <Image
              src={`https://web.poecdn.com${imagesRef[currency]}`}
              style={{ "max-height": "40px", "max-width": "40px" }}
            ></Image>
            {
              index === 0 &&
              <text>{`x ${amt["startCurr"]}`}</text>
            }
            {
              index !== 0 &&
              <text>{`x ${amt[currencies[index]]}`}</text>
            }

          </div>
        );
      })}
    </Col>
    <Col xl={2}style={{ "text-align": "right" }}>
      {whispers.map((whisper) => (
        <div>{whisper["info"]["name"]}</div>
      ))}
    </Col>
  </Container>
);
}

export default ListingHeader;