import Text.Printf
import Control.Exception
import System.CPUTime
import Numeric
import Data.List

-- | Creates list of groups of length `n` from a list
grp :: Int -> [a] -> [[a]]
grp _ [] = []
grp n xs =
    let (ys, zs) = splitAt n xs
    in  ys : grp n zs

-- | Creates some amt of equal length chunks
chunk :: Int -> [a] -> [[a]]
chunk amt xs = let chunksize = round $ (fromIntegral (length xs)) / fromIntegral amt
               in grp chunksize xs

-- | Group and sort a string
grpsort :: (Ord a) => Int -> [a] -> [[a]]
grpsort size xs = sort $ grp size xs

-- | Counts occurrences of element groups
countocc :: (Ord a) => [[a]] -> [([a],Float)]
countocc xs = map (\x -> (head x, fromIntegral (length x))) $ group $ sort xs

-- | Counts groups frequencies
--frequency :: Ord a => Int -> [a] -> [([a], Float)]
--frequency size xs =
--  let grps = grp size xs
--      occ = countocc grps
--      n = length grps in
--  map (\x -> (fst x, snd x / fromIntegral n)) (occ)

-- | Calculate one element of infomation summation
infoelem :: Float -> Float -> Float
infoelem p n = n * (-p) * (log(p)/log(2))

-- | Calculate information in string with sized groupings of characters
information size xs =
  let grps = grp size xs
      occ = countocc grps
      totalChars = fromIntegral (length grps) in
  sum $ map (\x -> (let n = snd x
                        p = n / totalChars in 
                    (infoelem p n))) (occ)

-- | Prints a float without scientific notation
showFullPrecision :: Float -> String
showFullPrecision x = showFFloat Nothing x ""

-- | Calculates information in string with sized character groups
processFile :: Int -> String -> IO ()
processFile size str = putStrLn $ showFullPrecision $ information size str

-- | Calculates run time of a function
time :: IO t -> IO t
time a = do
  start <- getCPUTime
  v <- a
  end   <- getCPUTime
  let diff = (fromIntegral (end - start)) / (10^12)
  printf "Computation time: %0.3f sec\n" (diff :: Double)
  return v

-- | Runs the information calculation for 1, 2, and 3 character long groups
runAllSizes s = do
  processFile 1 s
  processFile 2 s
  processFile 3 s

testReduce xs = let n = sum $ map (\x -> snd x) xs in
              map (\x -> (fst (fst x), n))

main = do
  s <- readFile "WarAndPeace.txt"
  time $ runAllSizes s
