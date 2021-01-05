import {React, useState} from 'react';
import { Accordion, Card, Button, Container, Row, InputGroup, FormControl, Col, Image, OverlayTrigger, Tooltip } from 'react-bootstrap'

import ListingHeader from './ListingHeader'
import '../App.css'
function Listings({ listings, imagesRef }) {
  const [copied, setCopied] = useState(true)
  function getWhispers(listing) {
    const whispers = [];
    for (let index = 1; index < listing["trades"].length; index += 1) {
      for (let j = 0; j < listing["listings"][listing["trades"][index]].length; j += 1) {
        const listingInfo = listing["listings"][listing["trades"][index]][j];
        const orderSize = listingInfo["order_size"];
        let whisper = listingInfo["info"]["whisper"]
        whisper = whisper.replace("{0}", listingInfo["info"]["has"]["min_amount"] * orderSize)
        whisper = whisper.replace("{1}", listingInfo["info"]["want"]["min_amount"] * orderSize)
        whispers.push({
          "whisper": whisper,
          "have": {
            "amount": listingInfo["info"]["has"]["min_amount"] * orderSize,
            "image": imagesRef[listing["trades"][index]]
          },
          "want": {
            "amount": listingInfo["info"]["want"]["min_amount"] * orderSize,
            "image": imagesRef[listing["trades"][index - 1]]
          }
        })
      }
    }
    console.log(whispers)
    return whispers;
  }
  function copyText(event) {
    event.preventDefault();
    event.target.parentElement.parentElement.children[1].select();
    document.execCommand('copy')
    // setCopied(true)
  }
  return (
    <Container>
      <Row>
        <Accordion style={{ "width": "100%" }}>
          {listings.map((trade) => {
            console.log(trade)
            console.log(trade['listings'][trade['trades'][1]][0]['info']['whisper'])
            // const key = Math.floor(Math.random() * 100);
            const key = trade["listings"][trade["trades"][1]][0]["info"]["posted"] * Math.floor(Math.random() * 10000);
            return (<Card style={{ "background": "#333333", "color": "white" }}>
              <Accordion.Toggle as={Card.Header} eventKey={key} style={{ "min-height": "10vh", "justify-content": "center", "display": "flex" }}>
                <ListingHeader tradeInfo={trade} imagesRef={imagesRef} />
              </Accordion.Toggle>
              <Accordion.Collapse eventKey={key}>
                <Row className="accordion-collapse" style={{ "display": "flex", "justify-content": "center" }}>
                  {getWhispers(trade).map((whisper) =>
                    <Row style={{ "width": "90%" }}>
                      <Col lg={2}>
                        <Image
                          src={`https://web.poecdn.com${whisper["want"]["image"]}`}
                          style={{ "max-height": "40px", "max-width": "40px" }}
                        ></Image>
                        <span>x {whisper["want"]["amount"]}</span>
                      </Col>
                      <Col lg={8}>
                        <InputGroup>
                          <InputGroup.Prepend>
                            <InputGroup.Checkbox />
                            <OverlayTrigger
                              key={whisper["whisper"]}
                              overlay={
                                <Tooltip id="tooltip-id">
                                  Copy
                                </Tooltip>
                              }
                            >
                              <Button className="fa fa-copy whisper-copy" onClick={(e) => copyText(e)} ></Button>
                            </OverlayTrigger>
                          </InputGroup.Prepend>
                          <FormControl defaultValue={whisper["whisper"]} />
                        </InputGroup>
                      </Col>
                      <Col lg={2}>
                        <Image
                          src={`https://web.poecdn.com${whisper["have"]["image"]}`}
                          style={{ "max-height": "40px", "max-width": "40px" }}
                        ></Image>
                        <span>x {whisper["have"]["amount"]}</span>
                      </Col>
                    </Row>
                  )}
                </Row>
              </Accordion.Collapse>
            </Card>)
          })}
        </Accordion>
      </Row>
    </Container>
  )
}

export default Listings;