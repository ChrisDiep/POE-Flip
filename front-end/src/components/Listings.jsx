import React from 'react';
import { Accordion, Card, Button } from 'react-bootstrap'

import ListingHeader from './ListingHeader'

function Listings({ listings, imagesRef }) {
  return (
    <Accordion style={{ "width": "100%" }}>
      {listings.map((trade) => {
        const key = Math.floor(Math.random() * 10);
        return (<Card>
          <Accordion.Toggle as={Card.Header} eventKey={key}>
            <ListingHeader tradeInfo={trade} imagesRef={imagesRef}/>
          </Accordion.Toggle>
          <Accordion.Collapse eventKey={key}>
            <Card.Body>
              {trade["total_profit"]}
            </Card.Body>
          </Accordion.Collapse>
        </Card>)
      })}
    </Accordion>
  )
}

export default Listings;