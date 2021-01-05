import React from 'react';
import { Accordion, Card, Button, Container, Row } from 'react-bootstrap'

import ListingHeader from './ListingHeader'

function Listings({ listings, imagesRef }) {
  return (
    <Container>
      <Row>
        <Accordion style={{ "width": "100%" }}>
          {listings.map((trade) => {
            const key = Math.floor(Math.random() * 100);
            return (<Card>
              <Accordion.Toggle as={Card.Header} eventKey={key}>
                <ListingHeader tradeInfo={trade} imagesRef={imagesRef} />
              </Accordion.Toggle>
              <Accordion.Collapse eventKey={key}>
                <Card.Body>
                  {trade["total_profit"]}
                </Card.Body>
              </Accordion.Collapse>
            </Card>)
          })}
        </Accordion>
      </Row>
    </Container>
  )
}

export default Listings;