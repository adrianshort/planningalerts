# Introduction #
Proposed development of a scraper for the Plan-It system.

# Authorities #

  * ~~Hounslow: http://planning.hounslow.gov.uk/planningv2/planning_search.aspx~~
  * ~~Kingston: http://maps.kingston.gov.uk/isis_main/planning/planning_search.aspx~~
  * Richmond (London): http://www2.richmond.gov.uk/PlanData2/Planning_Search.aspx
  * Wiltshire: http://www.wiltshireplanningapplications.co.uk/planning_search.aspx

# Notes #

  * There is a limit in the search form to the number of queries but this is not validated in software (tested with Richmond). It is therefore possible to search for a larger number of applications than the maximum of 500.
  * There are distinct differences between the implementations that means that a generic scraper will not work easily. Since scrapers exist for Hounslow and Kingston the plan is now to create a generic scraper (or one for each) for the remaining two authorities on this system.