#!/usr/bin/env wolframscript
(* ::Package:: *)

FeynRulesPath = "~/FeynRules";
ModelPath = "~/FeynRules/Models/Clockwork";
$FeynRulesPath=SetDirectory[FeynRulesPath];
<<FeynRules`;
SetDirectory[ModelPath];
LoadModel["SM.fr","Clockwork.fr"];
LoadRestriction["Massless.rst","DiagonalCKM.rst"];
WriteUFO[LFull];
