import { React, useState, useEffect } from 'react';
import { Col, Row, Container, Card } from "react-bootstrap"
import Selection from '../components/Selection'
import Listings from '../components/Listings'
import dummy from '../components/dummy'
import '../App.css'
function Landing() {
  const [listings, setListings] = useState(null)
  const [staticInfo, setStaticInfo] = useState(dummy.static.slice(0, 10))
  const [imagesRef, setImagesRef] = useState(createImagesRef(staticInfo))

  function createImagesRef(data) {
    return dummy.static.slice(0, 10).reduce((acc, category) => {
      category["entries"].forEach((entry) => acc[entry["text"]] = entry["image"])
      return acc;
    }, {})
  }
  function getListings() {
    setListings(dummy.listings)
  }
  return (
    <Card className="landing-card" bg="dark">
      <Card.Body>
        {/* <Container className="landing-container"> */}
        <Row className="justify-content-center selection-row" style={{ "width": "95%" }}>
          <Selection getListings={getListings} staticInfo={staticInfo}></Selection>
        </Row>
        {listings
          && <Row className="listings-row" style={{ "margin-top": "10px", "width": "95%" }}>
            <Listings listings={listings} imagesRef={imagesRef}></Listings>
          </Row>}
        {/* </Container> */}
      </Card.Body>
    </Card>
  );
}

export default Landing