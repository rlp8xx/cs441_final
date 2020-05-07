import Control.Exception
import System.CPUTime
import Text.Printf
import Control.Parallel.Strategies
import Numeric
import Data.List as List
import Data.Map.Strict as Map
import System.Environment

-- | Creates list of groups of length `n` from a list
grp :: Int -> [a] -> [[a]]
grp _ [] = []
grp n xs =
    let (ys, zs) = List.splitAt n xs
    in  ys : grp n zs

-- | Creates map with grouped string
mapgrp size xs = group $ List.sort $ grp size xs

-- | Count groups
cntgrp :: [[a]] -> [(a, Int)]
cntgrp xs = List.map (\x -> (head x, length x)) xs

-- | Creates some amt of equal length chunks
chunk :: Int -> [a] -> [[a]]
chunk amt xs = let chunksize = round $ (fromIntegral (length xs)) / fromIntegral amt
               in grp chunksize xs

-- | Cut xs into chunks, create spark for mapping cntgrp $ mapgrp onto each chunk
parcnt chunks size xs = parMap rseq (\x -> cntgrp $ mapgrp size x) (chunk chunks xs)

-- | Calculate one element of infomation summation
infoelem :: Int -> Int -> Float
infoelem n total = let n' = fromIntegral n
                       total' = fromIntegral total
                       p = n' / total'
                   in n' * (-p) * (log(p)/log(2))

-- | Calculate element-wise information in a frequency map
infomap m = let n = fromIntegral $ sum $ Map.elems m
             in fromList (List.map (\x -> (fst x, infoelem (snd x) n)) (Map.toList m))

-- | Calculate element-wise information in frequency list
parinfomapelem n m = List.map (\x -> infoelem (snd x) n) m

-- | 
parinfomap chunks m = let n = fromIntegral $ sum $ List.map (\x -> snd x) m
               in sum $ concat $ parMap rseq (\x -> parinfomapelem n x) (chunk chunks m)

-- | Put chunks from parcnt back together into a Data.Map.Strict object
chunkmap xs = fromListWith (+) (concat xs)

-- | Sum element-wise information in map
suminfomap m = sum $ List.map (\x -> snd x) (toList $ infomap m)

-- | Prints a float without scientific notation
showFullPrecision :: Float -> String
showFullPrecision x = showFFloat Nothing x ""

-- | Calculates information in string with sized character groups
processFile :: Int -> Int -> String -> IO ()
processFile chunks size str = putStrLn $ showFullPrecision $ parinfomap chunks $ toList $ chunkmap $ parcnt chunks size str

-- | Get single int arg
getIntArg :: IO Int
getIntArg = fmap (read . head) getArgs

-- | Calculates run time of a function
time :: IO t -> IO t
time a = do
  start <- getCPUTime
  v <- a
  end   <- getCPUTime
  let diff = (fromIntegral (end - start)) / (10^12)
  printf "Computation time: %0.3f sec\n" (diff :: Double)
  return v

-- | Runs for singles, pairs, and triples
runAllSizes chunks s = do
  processFile chunks 1 s
  processFile chunks 2 s
  processFile chunks 3 s

main = do
  chunks <- fmap (read . head) getArgs :: IO Int
  s <- readFile "WarAndPeace.txt"
  time $ runAllSizes chunks s
