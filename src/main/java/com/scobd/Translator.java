package com.scobd;

import java.io.*;

public class Translator
{
	public static void main(String[] args)
	{
		
		if(args.length < 2)
		{
			System.err.println("Usage: Translator <path-to-PML-file> <output-path>");
			System.exit(1);
		}
		String params[] = args;
				
		String filepath_in = params[0];
		String filepath_out = params[1];
		System.out.println("Input file: " + filepath_in);
		System.out.println("Output path: " + filepath_out);
		
		BufferedReader br = null;
		BufferedWriter bw = null;
		
		try
		{
			br = new BufferedReader(new FileReader(filepath_in));
			System.out.println("input file opened successfully!");
			bw = new BufferedWriter(new FileWriter(filepath_out));
			System.out.println("output file opened successfully!");

		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
		finally
		{
			if (br != null)
			{
				try
				{
					br.close();
				} catch (IOException e)
				{
					e.printStackTrace();
				}
			}
			if (bw != null)
			{
				try
				{
					bw.close();
				} catch (IOException e)
				{
					e.printStackTrace();
				}
			}
		}
	}
}