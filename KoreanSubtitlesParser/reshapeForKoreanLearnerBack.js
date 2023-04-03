const fs = require("fs");
const path = require("path");
const subDirectory = "subtitles/json";
const dirPath = path.join(__dirname, subDirectory);

const koPattern = /ko_\d+\.json/; // Matches strings like 'ko_1.json', 'ko_2.json', etc.
const zhPattern = /zh_\d+\.json/; // Matches strings like 'zh_1.json', 'zh_2.json', etc.
const showPattern = /[^_\W]+/g;

const jsonFiles = fs.readdirSync(dirPath);
const koFiles = jsonFiles.filter((file) => koPattern.test(file));
const zhFiles = jsonFiles.filter((file) => zhPattern.test(file));

const showName = koFiles[0].match(showPattern)[0];
const outputFileName = `${showName}_all.json`;
const outputFilePath = path.join(dirPath, outputFileName);

/** Sort by epsido num */
[koFiles, zhFiles].forEach((arr) => {
  arr.sort((a, b) => {
    const aNum = parseInt(a.match(/\d+/)[0]);
    const bNum = parseInt(b.match(/\d+/)[0]);
    return aNum - bNum;
  });
});

// jsonMerged[0] = [
//   ...,
//   {
//     chunckId: 85,
//     startTime: "00:04:06.875",
//     subtitles: ["나는 골프 뭐라는 줄 알고", "[로꼬가 웃는다]"],
//     pos: [[Array], [Array]],
//     subtitlesZh: ["原來這樣", "我以為你要說高爾夫球"],
//   },
// ];
/** Merge koFiles and zhFiles */
const jsonMerged = [];
for (let i = 0; i < koFiles.length; i++) {
  const jsonDataKo = require(path.join(dirPath, koFiles[i]));
  const jsonDataZh = require(path.join(dirPath, zhFiles[i]));
  const merged = jsonDataKo.map((entity1) => {
    const entity2 = jsonDataZh.find(
      (entity) => entity.chunckId === entity1.chunckId
    );
    return { ...entity1, subtitlesZh: entity2.subtitles };
  });
  jsonMerged.push(merged);
}

// var expect = {
//   show: "PaikSpirit",
//   episodes: [
//     [
//       /** index === 1, means it's ep1 */
//       ...{},
//       {
//         /** index === 1233, means it's chunckId === 1233 */
//         startTime: "00:58:54.666",
//         subtitles: ["내가 목요일날 끓여서 너한테 줄게"],
//         subtitlesZh: ["我週四會煮給你"],
//         pos: [
//           [
//             ["내가/NNG"],
//             ["목요일/NNG"],
//             ["날/NNG"],
//             ["끓이/VV", "어서/ECD"],
//             ["너/NP", "한테/JKO"],
//             ["주/VXV", "ㄹ게/EFN"],
//           ],
//           [],
//         ],
//       },
//     ],
//   ],
// };
/** Reformat / Reshape to expected format */
const expect = {};
expect.show = showName;
expect.episodes = [];
jsonMerged.forEach((merged, i) => {
  expect.episodes.push([]);
  expect.episodes[i] = merged.map((chunck) => {
    return {
      startTime: chunck.startTime,
      subtitles: chunck.subtitles,
      subtitlesZh: chunck.subtitlesZh,
      pos: chunck.pos,
    };
  });
});
console.log(
  `Done processing ${expect.episodes.length} episodes of show: ${expect.show}`
);

fs.writeFile(outputFilePath, JSON.stringify(expect), (err) => {
  if (err) throw err;
  console.log("Done written to file -> ", outputFilePath);
});
