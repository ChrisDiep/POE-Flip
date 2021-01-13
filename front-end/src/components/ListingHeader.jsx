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
      for (let j = 0; j < listings[currencies[index]].length; j += 1) {
        whispers.push(listings[currencies[index]][j])
        amt[currencies[index]] += listings[currencies[index]][j]["order_size"] * listings[currencies[index]][j]["info"]["has"]["min_amount"]
      }
    }
  }
  console.log(amt)
  return (
    <Container style={{ "display": "flex", "align-items": "center" }}>
      <Col xl={3} style={{ "text-align": "left" }}>
        <div
          style={{ "color": `${tradeInfo["total_profit"] > 0 ? "rgb(66, 181, 129)" : "red"}` }}
        >
          {`Total Profit: ${tradeInfo['total_profit']}`}
        </div>
        <div>{`Profit per Trade: ${tradeInfo['profit_per_trade']}`}</div>
      </Col>
      <Col xl={7}>
        {currencies.map((currency, index) => {
          console.log(`Index: ${index} Whisper: ${whispers[index]}`)
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
      <Col xl={2} style={{ "text-align": "right" }}>
        {whispers.map((whisper) => (
          <div>
            {whisper["info"]["status"] === "online" &&
              <svg height="24" viewBox="0 0 24 24" width="24" style={{ "fill": "rgb(66,181,129)" }}>
                <circle cx="12" cy="12" r="5"></circle>
              </svg>
            }
            {whisper["info"]["status"] === "afk" &&
              <svg height="14" viewBox="0 0 24 24" width="14" style={{ "transform": "rotate(45deg)", "fill": "rgb(250,166,25)", "margin-right": "5px", "margin-bottom": "2px" }}>
                <path d="M10 2c-1.82 0-3.53.5-5 1.35C7.99 5.08 10 8.3 10 12s-2.01 6.92-5 8.65C6.47 21.5 8.18 22 10 22c5.52 0 10-4.48 10-10S15.52 2 10 2z"></path>
              </svg>}
            <span>{whisper["info"]["name"]}</span>
          </div>
        ))}
      </Col>
    </Container>
  );
}

export default ListingHeader;