import React from 'react';
import { Container, Row, Col, Image } from 'react-bootstrap';

function ListingHeader({ tradeInfo, imagesRef }) {
  const currencies = tradeInfo['trades'];
  const listings = tradeInfo['listings'];
  const listingsCurr = Object.keys(listings)
  const whispers = [];
  const amt = {};
  //Iterates through currency
  for (let i = 0; i < listingsCurr.length; i += 1) {
    //Iterates through whispers
    for (let j = 0; j < listings[listingsCurr[i]].length; j += 1) {
      const whisper = listings[listingsCurr[i]][j];
      if (amt.hasOwnProperty("startingCurr")) {
        if (i === 0) {
          amt["startingCurr"] += whisper["order_size"] * whisper["info"]["want"]["min_amount"]
        }
      } else {
        amt["startingCurr"] = whisper["info"]["want"]["min_amount"]
      }
      if (amt.hasOwnProperty(listingsCurr[i])) {
        if (i !== 0) {
          amt[listingsCurr[i]] += whisper["info"]["want"]["min_amount"]
        }
      } else {
        if (i !== 0) {
          amt[listingsCurr[i]] = whisper["info"]["want"]["min_amount"]
        }
      }
      whispers.push(whisper)
    }
  }
  console.log(amt)
  return (
    <Container style={{ "display": "flex", "align-items": "center" }}>
      <Col style={{ "text-align": "left" }}>
        <div>{`Total Profit: ${tradeInfo['total_profit']}`}</div>
        <div>{`Profit per Trade: ${tradeInfo['profit_per_trade']}`}</div>
      </Col>
      <Col>
        {currencies.map((currency, index) => {
          console.log(`Index: ${index} Whisper: ${whispers[index]}`)
          const firstOrLast = index === 0 || index === currencies.length - 1;
          return (
            <div style={{ "display": "inline" }}>
              {index !== 0 &&
                <span className={'fa fa-arrow-right'}></span>}
              <Image
                src={`https://web.poecdn.com${imagesRef[currency]}`}
                style={{ "max-height": "40px", "max-width": "40px" }}
              ></Image>
              {
                index === 0 &&
                <text>{`x ${whispers[index]["order_size"] * whispers[index]["info"]["want"]["min_amount"]}`}</text>
              }
              {
                index === currencies.length - 1 &&
                <text>{`x ${whispers[index - 1]["order_size"] * whispers[index - 1]["info"]["want"]["min_amount"]}`}</text>
              }
              {
                index > 0 && !firstOrLast &&
                <text>{`x ${whispers[index - 1]["order_size"] * whispers[index - 1]["info"]["has"]["min_amount"]}`}</text>
              }
            </div>
          );
        })}
      </Col>
      <Col style={{ "text-align": "right" }}>
        {whispers.map((whisper) => (
          <div>{whisper["info"]["name"]}</div>
        ))}
      </Col>
    </Container>
  );
}

export default ListingHeader;