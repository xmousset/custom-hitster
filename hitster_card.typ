#import "@preview/zebra:0.1.0": qrcode

#set page(height: 5cm, width: 5cm, margin: 3mm)
#set text(font: "Orkney", size: 12pt)

#let hitster_card(
  spotify_link,
  track_year,
  track_title,
  artists,
  friend_who_add_it
) = {
  align(center + horizon)[
    #qrcode(spotify_link, height: 3cm)
  ]

  pagebreak()

  align(center + top)[
    #text(weight: 300)[#track_title]
  ]

  place(center + horizon)[
    #text(weight: 700, size: 28pt)[#track_year]
  ]

  align(center + bottom)[
    #text(weight: 400)[#artists]
  ]

  if friend_who_add_it != none {
    place(right + horizon, dx: 7mm)[#rotate(-90deg)[
      _#text(fill: luma(60%), size: 9pt, weight: 300)[#friend_who_add_it]_
    ]]
  }
}

#let hitster_deck(
  list_links,
  list_years,
  list_titles,
  list_artists,
  list_friends
) = {
  for i in range(list_links.len()) {
    hitster_card(
      list_links.at(i),
      list_years.at(i),
      list_titles.at(i),
      list_artists.at(i),
      list_friends.at(i),
    )
  }
}

#let get_input_list(input_idx) = {
  return (
    sys.inputs.at("url_" + str(input_idx), default: "https://github.com/xmousset"),
    sys.inputs.at("year_" + str(input_idx), default: "2026"),
    sys.inputs.at("name_" + str(input_idx), default: "Amazing Track"),
    sys.inputs.at("artists_" + str(input_idx), default: "Great Artist"),
    sys.inputs.at("added_by_name_" + str(input_idx), default: "Friend"),
  )
}

// Main loop

#let nb_tracks = int(sys.inputs.at("nb_tracks", default: 1))

#for i in range(nb_tracks) {
  let (url, year, name, artists, added_by_name) = get_input_list(i)
    hitster_card(
      url,
      year,
      name,
      artists,
      added_by_name,
    )
    if i < nb_tracks - 1 {
      pagebreak()
    }
  }
