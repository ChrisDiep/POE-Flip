import React from 'react';
import {Container, Row, Col, Image} from 'react-bootstrap';

function ListingHeader({ tradeInfo, imagesRef }) {
  const currencies = Object.keys(tradeInfo['listings']);
  const listings = tradeInfo['listings']
  return (
    <Container>
      {currencies.map((currency) =>
        <Image src={`https://web.poecdn.com${imagesRef[currency]}`}></Image>
      )}
    </Container>
  );
}

export default ListingHeader;