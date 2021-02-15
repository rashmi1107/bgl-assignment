# bgl-assignment

## Build info:
    Build:
    docker build -t bgl_test .
    Run:
    docker run -p 5000:5000 bgl_test

## Api Interface:
    ETH transfer
      - Method: `POST`
      - Endpoint: `/transact/ether`
      # transfers ETH from account1 to account2
   
    Custom ERC20 token transfer
      - Method: `POST`
      - Endpoint: `/transact/myTKN`
      # transfers TKN from account1 to account2

    View transactions
      - Method: `GET`
      - Endpoint: `/viewReportJSON/{address}`
      # returns txns from address
  
## Note:
    - concurrency is not handled for any API.
    - config file can be edited to change addresses for testing (corresponding keys to be updated; keys exposed for assignment purpose).
  
