<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <body>
    <?php
    $scriptName = "AboutMe.php";
    include("PHPprinter.php");
    $startTime = getMicroTime();
    
    $nickname = $_POST['nickname'];
    if ($nickname == null)
    {
      $nickname = $_GET['nickname'];
      if ($nickname == null)
      {
         printError($scriptName, $startTime, "About me", "You must provide your nick name!<br>");
         exit();
      }
    }
    $password = $_POST['password'];
    if ($password == null)
    {
      $password = $_GET['password'];
      if ($password == null)
      {
         printError($scriptName, $startTime, "About me", "You must provide your password!<br>");
         exit();
      }
    }
      
    getDatabaseLink($link);

    begin($link);
    // Authenticate the user 
    $userId = authenticate($nickname, $password, $link);
    if ( userId == -1)
    {
      rollback($link);
      die("<h2>ERROR: You don't have an account on RUBis! You have to register first.</h2><br>");
    }

    $userResult = mysqlQuery("SELECT * FROM users WHERE users.id=$userId", $link) or die("ERROR: Query failed");
    if (mysqli_num_rows($userResult) == 0)
    {
      rollback();
      die("<h3>ERROR: Sorry, but this user does not exist.</h3><br>\n");
    }

   printHTMLheader("RUBiS: About me");

      // Get general information about the user
    $userRow = mysqli_fetch_array($userResult);
    $firstname = $userRow["firstname"];
    $lastname = $userRow["lastname"];
    $nickname = $userRow["nickname"];
    $email = $userRow["email"];
    $creationDate = $userRow["creation_date"];
    $rating = $userRow["rating"];

    printHTMLHighlighted("<h2>Information about ".$nickname."<br></h2>");
    print("Real life name : ".$firstname." ".$lastname."<br>");
    print("Email address  : ".$email."<br>");
    print("User since     : ".$creationDate."<br>");
    print("Current rating : <b>".$rating."</b><br><p>");

     // Get the items the user has bid on
    $bidsResult = mysqlQuery("SELECT item_id, bids.max_bid FROM bids, items WHERE bids.user_id=$userId AND bids.item_id=items.id AND items.end_date>=NOW() GROUP BY item_id", $link) or die("ERROR: Query failed for getting bids list.");
    if (mysqli_num_rows($bidsResult) == 0)
      printHTMLHighlighted("<h2>You did not bid on any item.</h2>\n");
    else
    {
      printHTMLHighlighted("<h3>Items you have bid on.</h3>\n");
      print("<TABLE border=\"1\" summary=\"Items You've bid on\">\n".
                "<THEAD>\n".
                "<TR><TH>Designation<TH>Initial Price<TH>Current price<TH>Your max bid<TH>Quantity".
                "<TH>Start Date<TH>End Date<TH>Seller<TH>Put a new bid\n".
                "<TBODY>\n");
      while ($bidsRow = mysqli_fetch_array($bidsResult))
      {
	$maxBid = $bidsRow["max_bid"];
	$itemId = $bidsRow["item_id"];
	$itemResult = mysqlQuery("SELECT * FROM items WHERE id=$itemId", $link) or die("ERROR: Query failed for item the user has put a bid on.");
	if (mysqli_num_rows($itemResult) == 0)
        {
          rollback();
	  die("<h3>ERROR: This item does not exist.</h3><br>\n");
        }
	  
//	  $currentPriceResult = mysqlQuery("SELECT MAX(bid) AS bid FROM bids WHERE item_id=$itemId", $link) or die("ERROR: Query failed for getting the item current price.");
//	  if (mysqli_num_rows($currentPriceResult) == 0)
//	    die ("ERROR: Cannot get the current price (sold item).");
//	  $currentPriceRow = mysqli_fetch_array($currentPriceResult);
	  $itemRow = mysqli_fetch_array($itemResult);
	  $currentPrice = $itemRow["max_bid"];
	  if ($currentPrice == null)
	    $currentPrice = "none";
	
	  $itemName = $itemRow["name"];
	  $itemInitialPrice = $itemRow["initial_price"];
	  $quantity = $itemRow["quantity"];
	  $itemReservePrice = $itemRow["reserve_price"];
	  $startDate = $itemRow["start_date"];
	  $endDate = $itemRow["end_date"];
	  $sellerId = $itemRow["seller"];

	  $sellerResult = mysqlQuery("SELECT nickname FROM users WHERE id=$sellerId", $link) or die("ERROR: Query failed for getting the seller nickname.");
	  if (mysqli_num_rows($sellerResult) == 0)
          {
            rollback($link);
	    die("<h3>ERROR: This seller does not exist.</h3><br>\n");
          }
	  $sellerRow = mysqli_fetch_array($sellerResult);
	  $sellerNickname = $sellerRow["nickname"];
	  
	  print("<TR><TD><a href=\"/PHP/ViewItem.php?itemId=".$itemId."\">".$itemName.
		"<TD>".$itemInitialPrice."<TD>".$currentPrice."<TD>".$maxBid."<TD>".$quantity.
		"<TD>".$startDate."<TD>".$endDate.
		"<TD><a href=\"/PHP/ViewUserInfo.php?userId=".$sellerId."\">".$sellerNickname.
		"<TD><a href=\"/PHP/PutBid.php?itemId=".$itemId."&nickname=".urlencode($nickname)."&password=".urlencode($password)."\"><IMG SRC=\"/PHP/bid_now.jpg\" height=22 width=90></a>\n");
	
	  mysqli_free_result($sellerResult);
	  mysqli_free_result($currentPriceResult);
	}
	mysqli_free_result($itemResult);
	print("</TBODY></TABLE><p>\n");
    }

     // Get the items the user won in the past 30 days
     $wonItemsResult = mysqlQuery("SELECT item_id FROM bids, old_items WHERE bids.user_id=$userId AND bids.item_id=old_items.id AND TO_DAYS(NOW()) - TO_DAYS(old_items.end_date) < 30 GROUP BY item_id", $link) or die("ERROR: Query failed for getting current sellings.");
     if (mysqli_num_rows($wonItemsResult) == 0)
         printHTMLHighlighted("<h3>You didn't win any item.</h3>\n");
     else
     {
       printHTMLHighlighted("<h3>Items you won in the past 30 days.</h3>\n");
       print("<p><TABLE border=\"1\" summary=\"List of items\">\n".
                "<THEAD>\n".
                "<TR><TH>Designation<TH>Price you bought it<TH>Seller".
                "<TBODY>\n");
       while ($wonItemsRow = mysqli_fetch_array($wonItemsResult))
       {
         $itemId = $wonItemsRow["item_id"];
         $itemResult = mysqlQuery("SELECT * FROM old_items WHERE id=$itemId", $link) or die("ERROR: Query failed for getting the items the user won.");
         if (mysqli_num_rows($itemResult) == 0)
          {
            rollback($link);
           die("<h3>This item does not exist.</h3><br>\n");
          }
         
         $itemRow = mysqli_fetch_array($itemResult);
         $currentPrice = $itemRow["max_bid"];
         if ($currentPrice == null)
          $currentPrice = "none";
         $itemName = $itemRow["name"];
         $sellerId = $itemRow["seller"];
         
         $sellerResult = mysqlQuery("SELECT nickname FROM users WHERE id=$sellerId", $link) or die("ERROR: Query failed for getting the seller nickname.");
         if (mysqli_num_rows($sellerResult) == 0)
          {
            rollback($link);
           die("<h3>ERROR: This seller does not exist.</h3><br>\n");
          }
         $sellerRow = mysqli_fetch_array($sellerResult);
         $sellerNickname = $sellerRow["nickname"];
         
         print("<TR><TD><a href=\"/PHP/ViewItem.php?itemId=".$itemId."\">".$itemName.
               "<TD>".$currentPrice.
               "<TD><a href=\"/PHP/ViewUserInfo.php?userId=".$sellerId."\">".$sellerNickname.
               "\n");
         
         mysqli_free_result($sellerResult);
         mysqli_free_result($currentPriceResult);
       }
       
       print("</TBODY></TABLE><p>\n");
     }

     // Get the items the user bought in the past 30 days
     $buyNowResult = mysqlQuery("SELECT * FROM buy_now WHERE buy_now.buyer_id=$userId AND TO_DAYS(NOW()) - TO_DAYS(buy_now.date)<=30", $link)or die("ERROR: Query failed for getting buy now list.");    
     if (mysqli_num_rows($buyNowResult) == 0)
       printHTMLHighlighted("<h3>You didn't buy any item in the past 30 days.</h3>\n");
     else
     {
       printHTMLHighlighted("<h3>Items you bought in the past 30 days.</h3>\n");
       print("<p><TABLE border=\"1\" summary=\"List of items\">\n".
             "<THEAD>\n".
             "<TR><TH>Designation<TH>Quantity<TH>Price you bought it<TH>Seller".
             "<TBODY>\n");
       while ($buyNowRow = mysqli_fetch_array($buyNowResult))
       {
         $itemId = $buyNowRow["item_id"];
         $itemResult = mysqlQuery("SELECT * FROM old_items WHERE id=$itemId", $link) or die("ERROR: Query failed for getting the item the user bought.");
         if (mysqli_num_rows($itemResult) == 0)
          {
            rollback($link);
           die("<h3>ERROR: This item does not exist.</h3><br>\n");
          }
                  
         $itemRow = mysqli_fetch_array($itemResult);
         $itemName = $itemRow["name"];
         $sellerId = $itemRow["seller"];
         $price = $itemRow["buy_now"]*$buyNowRow["qty"];
         
         $sellerResult = mysqlQuery("SELECT nickname FROM users WHERE id=$sellerId", $link) or die("ERROR: Query failed for getting the seller nickname.");
         if (mysqli_num_rows($sellerResult) == 0)
          {
            rollback($link);
           die("<h3>ERROR: This seller does not exist.</h3><br>\n");
          }
         $sellerRow = mysqli_fetch_array($sellerResult);
         $sellerNickname = $sellerRow["nickname"];
         
         print("<TR><TD><a href=\"/PHP/ViewItem.php?itemId=".$itemId."\">".$itemName.
               "<TD>".$buyNowRow["qty"]."<TD>$price".
               "<TD><a href=\"/PHP/ViewUserInfo.php?userId=".$sellerId."\">".$sellerNickname.
               "\n");
         
	  mysqli_free_result($sellerResult);
       }
       
       print("</TBODY></TABLE><p>\n");
     }

     // Get the items the user is currently selling
     $currentSellsResult = mysqlQuery("SELECT * FROM items WHERE items.seller=$userId AND items.end_date>=NOW()", $link) or die("ERROR: Query failed for getting current sellings.");
     if (mysqli_num_rows($currentSellsResult) == 0)
      printHTMLHighlighted("<h3>You are currently selling no item.</h3>\n");
     else
     {
       printHTMLHighlighted("<h3>Items you are selling.</h3>\n");
       print("<p><TABLE border=\"1\" summary=\"List of items\">\n".
                "<THEAD>\n".
                "<TR><TH>Designation<TH>Initial Price<TH>Current price<TH>Quantity<TH>ReservePrice<TH>Buy Now".
                "<TH>Start Date<TH>End Date\n".
                "<TBODY>\n");
       while ($currentSellsRow = mysqli_fetch_array($currentSellsResult))
       {
	   $itemName = $currentSellsRow["name"];
	   $itemInitialPrice = $currentSellsRow["initial_price"];
	   $quantity = $currentSellsRow["quantity"];
	   $itemReservePrice = $currentSellsRow["reserve_price"];
	   $buyNow = $currentSellsRow["buy_now"];
	   $endDate = $currentSellsRow["end_date"];
	   $startDate = $currentSellsRow["start_date"];
	   $itemId = $currentSellsRow["id"];
//	   $currentPriceResult = mysqlQuery("SELECT MAX(bid) AS bid FROM bids WHERE item_id=$itemId", $link) or die("ERROR: Query failed for getting the item current price (sold item).");
//	   if (mysqli_num_rows($currentPriceResult) == 0)
//	       die ("ERROR: Cannot get the current price (sold item).");
//	   $currentPriceRow = mysqli_fetch_array($currentPriceResult);
	   $currentPrice = $currentSellsResult["max_bid"]; 
	   if ($currentPrice == null)
	   	$currentPrice = "none";

	   print("<TR><TD><a href=\"/PHP/ViewItem.php?itemId=".$itemId."\">".$itemName.
                  "<TD>".$itemInitialPrice."<TD>".$currentPrice."<TD>".$quantity.
		  "<TD>".$itemReservePrice."<TD>".$buyNow.
                  "<TD>".$startDate."<TD>".$endDate."\n");

	   mysqli_free_result($currentPriceResult);
       }
       print("</TABLE><p>\n");
     }

     // Get the items the user sold the last 30 days
     $pastSellsResult = mysqlQuery("SELECT * FROM old_items WHERE old_items.seller=$userId AND TO_DAYS(NOW()) - TO_DAYS(old_items.end_date) < 30", $link) or die("ERROR: Query failed for getting sold items list.");
     if (mysqli_num_rows($pastSellsResult) == 0)
      printHTMLHighlighted("<h3>You didn't sell any item in the last 30 days.</h3>\n");
     else
     {
       printHTMLHighlighted("<h3>Items you sold in the last 30 days.</h3>\n");
       print("<p><TABLE border=\"1\" summary=\"List of items\">\n".
                "<THEAD>\n".
                "<TR><TH>Designation<TH>Initial Price<TH>Current price<TH>Quantity<TH>ReservePrice<TH>Buy Now".
                "<TH>Start Date<TH>End Date\n".
                "<TBODY>\n");
       while ($pastSellsRow = mysqli_fetch_array($pastSellsResult))
       {
	   $itemName = $pastSellsRow["name"];
	   $itemInitialPrice = $pastSellsRow["initial_price"];
	   $quantity = $pastSellsRow["quantity"];
	   $itemReservePrice = $pastSellsRow["reserve_price"];
	   $buyNow = $pastSellsRow["buy_now"];
	   $endDate = $pastSellsRow["end_date"];
	   $startDate = $pastSellsRow["start_date"];
	   $itemId = $pastSellsRow["id"];
// 	   $currentPriceResult = mysqlQuery("SELECT MAX(bid) AS bid FROM bids WHERE item_id=$itemId", $link) or die("ERROR: Query failed for getting the item current price (sold item).");
// 	   if (mysqli_num_rows($currentPriceResult) == 0)
// 	       die ("ERROR: Cannot get the current price (sold item).");

// 	   $currentPriceRow = mysqli_fetch_array($currentPriceResult);
	   $currentPrice = $pastSellsResult["max_bid"]; 
	   if ($currentPrice == null)
	   	$currentPrice = "none";

	   print("<TR><TD><a href=\"/PHP/ViewItem.php?itemId=".$itemId."\">".$itemName.
                  "<TD>".$itemInitialPrice."<TD>".$currentPrice."<TD>".$quantity.
		  "<TD>".$itemReservePrice."<TD>".$buyNow.
                  "<TD>".$startDate."<TD>".$endDate."\n");

	   mysqli_free_result($currentPriceResult);
       }
       print("</TABLE><p>\n");

     }

    // Get the comments about the user
    $commentsResult = mysqlQuery("SELECT * FROM comments WHERE comments.to_user_id=$userId", $link) or die("ERROR: Query failed for the list of comments.");
    if (mysqli_num_rows($commentsResult) == 0)
      printHTMLHighlighted("<h2>There is no comment for this user.</h2>\n");
    else
    {
	print("<p><DL>\n");
	printHTMLHighlighted("<h3>Comments about you.</h3>\n");
	while ($commentsRow = mysqli_fetch_array($commentsResult))
	{
	    $authorId = $commentsRow["from_user_id"];
	    $authorResult = mysqlQuery("SELECT nickname FROM users WHERE users.id=$authorId", $link) or die("ERROR: Query failed for the comment author.");
	    if (mysqli_num_rows($authorResult) == 0)
            {
              rollback($link);
              die("ERROR: This author does not exist.<br>\n");
            }
	    else
	    {
		$authorRow = mysqli_fetch_array($authorResult);
		$authorName = $authorRow["nickname"];
	    }
	    $date = $commentsRow["date"];
	    $comment = $commentsRow["comment"];
	    
	    print("<DT><b><BIG><a href=\"/PHP/ViewUserInfo.php?userId=".$authorId."\">$authorName</a></BIG></b>"." wrote the ".$date."<DD><i>".$comment."</i><p>\n");
	    mysqli_free_result($authorResult);
	}
	print("</DL>\n");

    }
    commit($link);
    mysqli_free_result($userResult);
    mysqli_free_result($commentsResult);
    mysqli_free_result($bidsResult);
    mysqli_free_result($currentSellsResult);
    mysqli_free_result($pastSellsResult);
    mysqli_free_result($wonItemsResult);
    mysqli_free_result($buyNowResult);
    mysqli_close($link);
    
    printHTMLfooter($scriptName, $startTime);
    ?>
  </body>
</html>
