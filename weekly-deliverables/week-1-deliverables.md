# Summary
Understood task prompt and goal of the project. Confirmed dataset access of the minimum  6 months of CRMLSSold files and reviewed metadata pdf that relate to the CRMLSSold files.

# Data Dictionary

| Field Name | Type | Size | Description |
|---|---|---|---|
| BuyerAgentAOR | AOR Enum | | The Buyer's Agent's Board or Association of REALTORS. |
| ListAgentAOR | AOR Enum | | The Listing Agent's Board or Association of REALTORS. |
| Flooring | Flooring Enum | | A list of the type(s) of flooring found within the property. |
| ViewYN | Boolean | | The property has a view. |
| WaterfrontYN | Boolean | | The property is on the waterfront. |
| BasementYN | Boolean | | Does the property have a basement? |
| PoolPrivateYN | Boolean | | The property has a privately owned pool that is included in the sale/lease. |
| OriginalListPrice | Decimal | 14.2 | The original price of the property on the initial agreement between the seller and the seller's broker. |
| ListingKey | String | 20 | A unique identifier for this record from the immediate source. This is a string that can include a Uniform Resource Identifier (URI) or other forms. This is the local key of the system. Records are received from other systems, a local key is commonly applied. If conveying the original keys from the source or originating systems, see SourceSystemKey and OriginatingSystemKey. |
| ListAgentEmail | String | 80 | The email address of the Listing Agent. |
| CloseDate | DateTime | | With for-sale listings, the date the purchase agreement was fulfilled. With lease listings, the date the requirements were fulfilled, such as contract and/or deposit. This is the date entered by the agent reflecting when the change occurred contractually, not a timestamp of when the change was made in the MLS. |
| ClosePrice | Decimal | 14.2 | The amount of money paid by the purchaser to the seller for property under the agreement. |
| ListAgentFirstName | String | 50 | The first name of the listing agent. |
| ListAgentLastName | String | 50 | The last name of the listing agent. |
| Latitude | Decimal | 12.8 | The geographic latitude of some reference point on the property, specified in degrees and decimal parts. Positive numbers must not include the plus symbol. |
| Longitude | Decimal | 12.8 | The geographic longitude of some reference point on the property, specified in degrees and decimal parts. Positive numbers must not include the plus symbol. |
| UnparsedAddress | String | 255 | The UnparsedAddress is a text representation of the address with the full civic location as a single entity. It may optionally include any of City, StateOrProvince, PostalCode and Country. |
| PropertyType | PropertyType Enum | | A list of types of properties such as Residential, Lease, Income, Land, Mobile, Commercial Sale, etc... |
| LivingArea | Decimal | 14.2 | The total livable area within the structure. |
| ListPrice | Decimal | 14.2 | The current price of the property as determined by the seller and the seller's broker. For auctions this is the minimum or reserve price. |
| DaysOnMarket | Int32 | 4 | The number of days the listing is on market, as defined by the MLS business rules. |
| ListOfficeName | String | 255 | The legal name of the brokerage representing the seller. |
| BuyerOfficeName | String | 255 | The legal name of the brokerage representing the buyer. |
| CoListOfficeName | String | 255 | The legal name of the brokerage co-representing the seller. |
| ListAgentFullName | String | 150 | The full name of the listing agent. (First Middle Last) |
| CoListAgentFirstName | String | 50 | The first name of the co-listing agent. |
| CoListAgentLastName | String | 50 | The last name of the co-listing agent. |
| BuyerAgentMlsId | String | 25 | The local, well-known identifier. This value may not be unique, specifically in the case of aggregation systems, this value should be the identifier from the original system. |
| BuyerAgentFirstName | String | 50 | The first name of the buyer's agent. |
| BuyerAgentLastName | String | 50 | The last name of the buyer's agent. |
| FireplacesTotal | Int32 | | The total number of fireplaces included in the property. |
| AssociationFeeFrequency | FeeFrequency Enum | | The frequency the association fee is paid. For example, Weekly, Monthly, Annually, Bi-Monthly, One Time, etc. |
| AboveGradeFinishedArea | Decimal | 14.2 | Finished area within the structure that is at or above the surface of the ground. |
| ListingKeyNumeric | Int64 | 10 | ListingKeyNumeric |
| MLSAreaMajor | String | 50 | The major marketing area name, as defined by the MLS or other non-governmental organization. If there is only one MLS Area in use, it must be the MLSAreaMajor. |
| TaxAnnualAmount | Decimal | 14.2 | The annual property tax amount as of the last assessment made by the taxing authority. |
| CountyOrParish | String | 50 | The County, Parish or other regional authority. |
| MlsStatus | MlsStatus Enum | | Local or regional status that are well known by business users. Each MlsStatus must map to a single StandardStatus. Multiple MlsStatus may map to a single StandardStatus. |
| ElementarySchool | String | 50 | The name of the primary school having a catchment area that includes the associated property. |
| AttachedGarageYN | Boolean | | A flag indicating that a garage is attached to the main/primary dwelling. If more than one garage structure exists, this field would be set to Yes if any of the garage structures were attached to the main structure. |
| ParkingTotal | Decimal | 14.2 | The total number of parking spaces included in the sale. |
| BuilderName | String | 50 | Name of the builder of the property or builder's tract. |
| PropertySubType | PropertySubType Enum | | A list of sub types to Residential, Residential Lease, Manufactured in Park, Commercial and Business Opportunity listings. e.g. Single Family Residence, Condominium, Manufactured on Land, Townhouse, Multi Family, Office, Retail, etc. |
| LotSizeAcres | Decimal | 16.4 | The total Acres of the lot. This field is related to the Lot Size Area and Lot Size Units and must be in sync with the values represented in those fields. Lot Size Source also applies to this field when used. |
| SubdivisionName | String | 50 | A neighborhood, community, complex or builder tract. |
| BuyerOfficeAOR | AOR Enum | | The buyer's office's board or association of REALTORS®. |
| YearBuilt | Int32 | 4 | The year that an occupancy permit is first granted for the house or other local measure of initial habitability of the build. The type definition permits an empty value with an attribute noting that it is an unknown date or that the building is new construction. While constraints have not been applied, convention at the time of adoption has this as a four (4) digit year value. |
| StreetNumberNumeric | Int32 | 4 | The integer portion of the street number. |
| ListingId | String | 255 | The well known identifier for the listing. The value may be identical to that of the Listing Key, but the Listing ID is intended to be the value used by a human to retrieve the information about a specific listing. In a multiple originating system or a merged system, this value may not be unique and may require the use of the provider system to create a synthetic value. |
| BathroomsTotalInteger | Int32 | 4 | The simple sum of the number of bathrooms. For example for a property with two Full Bathrooms and one Half Bathroom, the Bathrooms Total Integer will be 3. Expressing this example as 2.5, you will need to use a non-standard field name. Decimal based bathrooms are not recommended but possible with the Dictionary's extensibility. |
| City | String | 50 | The city in listing address. |
| TaxYear | Int32 | 50 | The year with the last assessment of property value/tax was made. |
| BuildingAreaTotal | Decimal | 14.2 | Total area of the structure. Includes both finished and unfinished areas. |
| BedroomsTotal | Int32 | 4 | The total number of bedrooms in the dwelling. |
| ContractStatusChangeDate | DateTime | | The date of the listings contractual status change. This is not necessarily the time the agent made the change in the MLS system, but rather the date of the contractual change. |
| ElementarySchoolDistrict | String | 50 | The name of the elementary school district having a catchment area that includes the associated property. |
| CoBuyerAgentFirstName | String | 50 | The first name of the buyer's co-agent. |
| PurchaseContractDate | DateTime | | With for-sale listings, the date an offer was accepted and the listing was no longer on market. This is the date entered by the agent reflecting when the change occurred contractually, not a timestamp of when the change was made in the MLS. With lease listings this may represent a meeting of the minds to lease, but some contractual requirements are yet to be fulfilled, such as contract signing or receipt of the deposit. |
| ListingContractDate | DateTime | | The effective date of the agreement between the seller and the listing agent reflecting when the change occurred contractually, not a timestamp of when the change was made in the MLS. |
| BelowGradeFinishedArea | Decimal | 14.2 | Finished area within the structure that is below ground. |
| BusinessType | BusinessType Enum | | The type of business being sold. Retail, Wholesale, Grocery, Food & Bev, etc. |
| StateOrProvince | StateOrProvince Enum | | Text field containing the accepted postal abbreviation for the state or province. |
| CoveredSpaces | Decimal | 14.2 | The total number of garage and carport spaces. |
| MiddleOrJuniorSchool | String | 50 | The name of the junior or middle school having a catchment area that includes the associated property. |
| FireplaceYN | Boolean | | Does the property include a fireplace. |
| Stories | Int32 | 4 | The number of floors in the property being sold. |
| HighSchool | String | 50 | The name of the high school having a catchment area that includes the associated property. |
| Levels | Levels Enum | | The number of levels in the property being sold. For example, One Level, Two Levels, Three or More Levels, Multi/Split, Loft. A discreet horizontal plane of interior living space (excluding basements). |
| LotSizeDimensions | String | 150 | The dimensions of the lot minimally represented as length and width (i.e. 250 x 180) or a measurement of all sides of the polygon representing the property lines of a residence (i.e. 30 x 50 x 120 x 60 x 22. |
| LotSizeArea | Decimal | 16.4 | The total area of the lot. See Lot Size Units for the units of measurement (Square Feet, Square Meters, acre, etc.). |
| MainLevelBedrooms | Int32 | 4 | The number of bedrooms located on the main or entry level of the property. |
| NewConstructionYN | Boolean | | Is the property newly constructed and has not been previously occupied? |
| GarageSpaces | Decimal | 14.2 | The number of spaces in the garage(s). |
| HighSchoolDistrict | String | 50 | The name of the high school district having a catchment area that includes the associated property. When only one school district is used, this should be used over the Junior or Elementary Districts. |
| PostalCode | String | 10 | The postal code portion of a street or mailing address. |
| AssociationFee | Decimal | 14.2 | A fee paid by the homeowner to the Home Owners Association which is used for the upkeep of the common area, neighborhood or other association related benefits. |
| LotSizeSquareFeet | Decimal | 14.2 | The total square footage of the lot. This field is related to the Lot Size Area and Lot Size Units and must be in sync with the values represented in those fields. Lot Size Source also applies to this field when used. |
| MiddleOrJuniorSchoolDistrict | String | 50 | The name of the junior or middle school district having a catchment area that includes the associated property. |
