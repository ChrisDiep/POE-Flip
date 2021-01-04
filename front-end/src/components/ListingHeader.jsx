import React from 'react';
import { Container, Row, Col, Image } from 'react-bootstrap';

function ListingHeader({ tradeInfo, imagesRef }) {
  const currencies = tradeInfo['trades'];
  const listings = tradeInfo['listings'];
  const listings_curr = Object.keys(listings)
  const whispers = [];
  for (let i = 0; i < listings_curr.length; i += 1) {
    for (let j = 0; j < listings[listings_curr[i]].length; j += 1) {
      whispers.push(listings[listings_curr[i]][j])
    }
  }
  console.log(whispers)
  return (
    <Container style={{ "display": "flex" }}>
      <Col className="justify-content-start">
        <div>{`Total Profit: ${tradeInfo['total_profit']}`}</div>
        <div>{`Profit per Trade: ${tradeInfo['profit_per_trade']}`}</div>
      </Col>
      <Col>
        {currencies.map((currency, index) => {
          return (
            <div style={{ "display": "inline" }}>
              {index !== 0 &&
                <span className={'fa fa-arrow-right'}></span>}
              <Image
                src={`https://web.poecdn.com${imagesRef[currency]}`}
                style={{ "max-height": "40px", "max-width": "40px" }}
              ></Image>
            </div>
          );
        })}
      </Col>
      <Col>
        {whispers.map((whisper) => (
          <div>{whisper["info"]["name"]}</div>
        ))}
      </Col>
    </Container>
  );
}

export default ListingHeader;